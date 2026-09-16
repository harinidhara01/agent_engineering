import os
import json
import sqlite3
import time
from datetime import datetime
from config import Config

def init_db():
    os.makedirs(os.path.dirname(Config.DB_PATH), exist_ok=True)
    os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
    os.makedirs(Config.DOCUMENTS_DIR, exist_ok=True)

    if not os.path.exists(Config.LOGS_PATH):
        with open(Config.LOGS_PATH, "w") as f:
            json.dump([], f)

    conn = sqlite3.connect(Config.DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chats (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            chat_id TEXT,
            role TEXT,
            content TEXT,
            citations TEXT,
            trace_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (chat_id) REFERENCES chats (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS documents (
            id TEXT PRIMARY KEY,
            filename TEXT,
            file_hash TEXT UNIQUE,
            file_type TEXT,
            chunk_count INTEGER,
            file_size INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_chunks (
            id TEXT PRIMARY KEY,
            document_id TEXT,
            filename TEXT,
            page INTEGER,
            section TEXT,
            chunk_index INTEGER,
            text TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (document_id) REFERENCES documents (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traces (
            id TEXT PRIMARY KEY,
            chat_id TEXT,
            user_request TEXT,
            agent_decision TEXT,
            tool_name TEXT,
            tool_input TEXT,
            tool_output TEXT,
            retrieved_chunks TEXT,
            gemini_model TEXT,
            final_response TEXT,
            duration_ms REAL,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def seed_sample_data():
    """Pre-populates sample policy documents if knowledge base is empty"""
    init_db()
    conn = sqlite3.connect(Config.DB_PATH)
    count = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
    conn.close()

    if count == 0:
        from rag import ingest_document
        sample_docs = [
            "Leave_Policy.txt",
            "Remote_Work_Policy.txt",
            "Travel_Expense_Policy.txt",
            "Benefits_Guide.txt",
            "Working_Hours_Policy.txt"
        ]
        for doc in sample_docs:
            path = os.path.join(Config.DOCUMENTS_DIR, doc)
            if os.path.exists(path):
                ingest_document(path, doc, replace_existing=True)

def log_execution(trace_id, component, call_type, inputs, outputs, duration_ms, status="success"):
    """Appends non-binary interaction logs to database/logs.json"""
    init_db()
    log_entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "trace_id": trace_id,
        "component": component,
        "call_type": call_type,
        "input": inputs,
        "output": outputs,
        "duration_ms": round(duration_ms, 2),
        "status": status
    }
    
    try:
        logs = []
        if os.path.exists(Config.LOGS_PATH):
            with open(Config.LOGS_PATH, "r") as f:
                logs = json.load(f)
        logs.append(log_entry)
        with open(Config.LOGS_PATH, "w") as f:
            json.dump(logs, f, indent=2)
    except Exception as e:
        print(f"Logging error: {e}")

def get_db_connection():
    conn = sqlite3.connect(Config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn
