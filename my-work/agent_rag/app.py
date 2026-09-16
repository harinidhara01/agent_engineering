import os
import uuid
import json
from flask import Flask, render_template, request, jsonify
from config import Config
from database import init_db, seed_sample_data, get_db_connection, log_execution
from rag import ingest_document
from agent import Agent

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database tables & directory structures
init_db()
seed_sample_data()

@app.route("/")
def index():
    return render_template("base.html")

# Chat endpoints
@app.route("/api/chats", methods=["GET", "POST"])
def chats():
    conn = get_db_connection()
    if request.method == "POST":
        chat_id = str(uuid.uuid4())
        conn.execute("INSERT INTO chats (id, title) VALUES (?, ?)", (chat_id, "New Conversation"))
        conn.commit()
        conn.close()
        return jsonify({"id": chat_id, "title": "New Conversation"})
    
    chats = conn.execute("SELECT * FROM chats ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(c) for c in chats])

@app.route("/api/chats/<chat_id>/messages", methods=["GET"])
def chat_messages(chat_id):
    conn = get_db_connection()
    messages = conn.execute("SELECT * FROM messages WHERE chat_id = ? ORDER BY created_at ASC", (chat_id,)).fetchall()
    conn.close()
    return jsonify([dict(m) for m in messages])

@app.route("/api/chat", methods=["POST"])
def process_chat():
    data = request.json or {}
    question = data.get("question", "").strip()
    chat_id = data.get("chat_id")

    if not question:
        return jsonify({"error": "Question text cannot be empty"}), 400

    if not chat_id:
        conn = get_db_connection()
        chat_id = str(uuid.uuid4())
        conn.execute("INSERT INTO chats (id, title) VALUES (?, ?)", (chat_id, question[:30]))
        conn.commit()
        conn.close()
    else:
        conn = get_db_connection()
        conn.execute("UPDATE chats SET title = ? WHERE id = ? AND title = 'New Conversation'", (question[:35], chat_id))
        conn.commit()
        conn.close()

    result = Agent.process_request(question, chat_id)
    return jsonify(result)

# Evidence endpoint
@app.route("/api/evidence/<trace_id>", methods=["GET"])
def get_evidence(trace_id):
    conn = get_db_connection()
    trace = conn.execute("SELECT * FROM traces WHERE id = ?", (trace_id,)).fetchone()
    conn.close()
    if not trace:
        return jsonify({"error": "Execution trace not found"}), 404
    return jsonify(dict(trace))

# Execution traces endpoint
@app.route("/api/traces", methods=["GET"])
def get_traces():
    conn = get_db_connection()
    traces = conn.execute("SELECT * FROM traces ORDER BY created_at DESC LIMIT 50").fetchall()
    conn.close()
    return jsonify([dict(t) for t in traces])

# Knowledge base document management
@app.route("/api/documents", methods=["GET"])
def get_documents():
    conn = get_db_connection()
    docs = conn.execute("SELECT * FROM documents ORDER BY created_at DESC").fetchall()
    total_chunks = conn.execute("SELECT COUNT(*) as count FROM document_chunks").fetchone()["count"]
    conn.close()
    return jsonify({
        "documents": [dict(d) for d in docs],
        "total_chunks": total_chunks
    })

@app.route("/api/documents/chunks/<doc_id>", methods=["GET"])
def get_document_chunks(doc_id):
    conn = get_db_connection()
    chunks = conn.execute("SELECT * FROM document_chunks WHERE document_id = ? ORDER BY chunk_index ASC", (doc_id,)).fetchall()
    conn.close()
    return jsonify([dict(c) for c in chunks])

@app.route("/api/documents/upload", methods=["POST"])
def upload_document():
    if "file" not in request.files:
        return jsonify({"error": "No file attached in request"}), 400
    
    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Invalid filename"}), 400

    replace = request.form.get("replace") == "true"
    temp_path = os.path.join(Config.DOCUMENTS_DIR, file.filename)
    file.save(temp_path)

    result = ingest_document(temp_path, file.filename, replace_existing=replace)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
