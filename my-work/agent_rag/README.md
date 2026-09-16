# Employee Policy Assistant

An intelligent, multi-tab enterprise web application built with **Flask**, **Google Gemini**, local vector embeddings, and RAG document search.

---

## 🌟 Features & Architecture

```text
             KNOWLEDGE BASE
                   │
              Upload Policy
                   ↓
              Duplicate Check (SHA-256)
                   ↓
                 Parse
                   ↓
                 Chunk
                   ↓
         Local Vector Indexing
                   ↓
                SQLite DB
                   │
                   │
USER ───────────► AGENT
│
┌─────┴─────┐
▼           ▼
RAG        TOOL
│           │
▼           ▼
Policy DB  Regional Holidays (No API key)
│           │
└─────┬─────┘
↓
Gemini LLM
↓
Answer + Inline Citation
│
┌──────┴──────┐
▼             ▼
Evidence       Execution Trace
```

### 1. **Assistant Tab**
- Interactive chat interface supporting multiple concurrent conversations.
- Sends user queries to backend Python Agent.
- RAG policy search against uploaded document database.
- Clickable inline `[Citation X]` links directing to full evidence pane.

### 2. **Evidence Tab**
- Dual-pane layout:
  - **Left Pane:** User question & Assistant response.
  - **Right Pane:** Source document metadata, page/section, and highlighted text chunk, OR tool execution inputs & returned evidence.
- Explicitly demarcates **Document Evidence** vs **Tool Evidence**.

### 3. **Execution Trace Tab**
- High-level flow visualization diagram.
- Detailed step-by-step logs including Trace ID, timestamp, component, status, execution duration, retrieved document chunks, tool calls, and Gemini model.
- Zero exposure of internal chain-of-thought or hidden reasoning.

### 4. **Knowledge Base Tab**
- Upload PDF, TXT, and DOCX policy documents.
- **SHA-256 Content Duplicate Detection**: Prevents duplicate ingestion even under different filenames, offering user options to cancel or replace.
- Document metrics (chunk count, size, hash, index status).
- **View Chunks Modal**: Detailed chunk inspection showing page, section, and text.

---

## 🚀 Quickstart Guide

### 1. Environment Configuration (`.env`)
```bash
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=database/vector_db
TOP_K=3
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### 2. Start the Application
```bash
# Navigate to project directory
cd my-work/agent_rag

# Run Flask Web Server
python3 app.py
```
Open your browser at: `http://localhost:5000`

---

## 📝 Sample Questions to Try

1. **Policy Question:** `What is the vacation policy?`
2. **Parental Leave:** `How many days of parental leave are available?`
3. **Remote Work:** `Can employees work remotely?`
4. **Reimbursement:** `What is the business meal reimbursement limit?`
5. **Tool Question:** `What holidays are observed in Ohio in 2026?`

---

## 🛠 Project Structure

```text
agent_rag/
├── app.py              # Flask server & web routes
├── agent.py            # Backend Agent & Gemini integration
├── rag.py              # Hash duplicate check, text extraction, chunking & RAG vector search
├── tools.py            # Policy search & regional holiday tools
├── database.py         # SQLite DB & database/logs.json execution logger
├── config.py           # Application settings loader
├── requirements.txt    # Dependencies
├── .env                # Secrets and configuration
├── .env.example        # Environment variable template
├── README.md           # Documentation
├── documents/          # Sample policy files
├── templates/          # HTML templates (base, tabs, modals)
└── static/             # Glassmorphism CSS & Single Page JS app
```
