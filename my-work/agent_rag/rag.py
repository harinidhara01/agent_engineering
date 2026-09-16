import os
import time
import hashlib
import uuid
import re
import math
from typing import List, Dict, Any, Tuple
from config import Config
from database import get_db_connection, log_execution

# Fallback text extraction helpers
def extract_text_from_pdf(file_path: str) -> List[Dict[str, Any]]:
    """Extract pages from PDF using pypdf or PyPDF2 if available, else plain text fallback"""
    pages = []
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages.append({"page": idx + 1, "text": text})
    except Exception:
        # Basic text fallback for simple files
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
        pages.append({"page": 1, "text": content})
    return pages

def extract_text_from_docx(file_path: str) -> List[Dict[str, Any]]:
    try:
        import docx
        doc = docx.Document(file_path)
        full_text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return [{"page": 1, "text": full_text}]
    except Exception:
        with open(file_path, "r", errors="ignore") as f:
            content = f.read()
        return [{"page": 1, "text": content}]

def extract_text_from_txt(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    return [{"page": 1, "text": content}]

def compute_file_hash(file_path: str) -> str:
    """Computes SHA-256 hash of file content"""
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_duplicate_document(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    """Checks if a document with identical SHA-256 hash already exists in DB"""
    file_hash = compute_file_hash(file_path)
    conn = get_db_connection()
    doc = conn.execute("SELECT * FROM documents WHERE file_hash = ?", (file_hash,)).fetchone()
    conn.close()
    if doc:
        return True, dict(doc)
    return False, {}

def chunk_text(pages: List[Dict[str, Any]], chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
    """Splits text pages into chunks with page, section, and index metadata"""
    chunks = []
    chunk_index = 0

    for page_info in pages:
        page_num = page_info["page"]
        text = page_info["text"]

        # Simple section detection (e.g. # Section, Section 1:, etc.)
        lines = text.split("\n")
        current_section = "General Policy"

        words = text.split()
        if not words:
            continue

        start = 0
        step = max(1, chunk_size - overlap)
        while start < len(words):
            chunk_words = words[start:start + chunk_size]
            chunk_str = " ".join(chunk_words)

            # Try to refine section header from text
            for line in lines:
                if line.strip().startswith("#") or line.strip().startswith("Section"):
                    current_section = line.strip().lstrip("#").strip()
                    break

            chunks.append({
                "chunk_index": chunk_index,
                "page": page_num,
                "section": current_section,
                "text": chunk_str
            })
            chunk_index += 1
            start += step

    return chunks

# Lightweight Vector Search Engine (Cosine Similarity on TF-IDF / Word Embeddings)
class SimpleVectorStore:
    """Local vector engine storing documents & chunks with metadata in SQLite and memory"""
    
    @staticmethod
    def _tokenize(text: str) -> Dict[str, float]:
        words = re.findall(r'\w+', text.lower())
        total = len(words) or 1
        tf = {}
        for w in words:
            tf[w] = tf.get(w, 0) + 1 / total
        return tf

    @staticmethod
    def _cosine_similarity(vec1: Dict[str, float], vec2: Dict[str, float]) -> float:
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        
        sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
        sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        
        if not denominator:
            return 0.0
        return numerator / denominator

def ingest_document(file_path: str, filename: str, replace_existing: bool = False) -> Dict[str, Any]:
    """Ingests a PDF/TXT/DOCX file into document repository and chunk database"""
    start_time = time.time()
    file_hash = compute_file_hash(file_path)
    is_dup, existing_doc = check_duplicate_document(file_path)

    conn = get_db_connection()

    if is_dup and not replace_existing:
        conn.close()
        return {
            "status": "duplicate",
            "message": f"Document already exists as '{existing_doc['filename']}'",
            "document": existing_doc
        }

    if is_dup and replace_existing:
        # Delete existing document chunks and record
        conn.execute("DELETE FROM document_chunks WHERE document_id = ?", (existing_doc["id"],))
        conn.execute("DELETE FROM documents WHERE id = ?", (existing_doc["id"],))
        conn.commit()

    # Determine file type
    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        pages = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        pages = extract_text_from_docx(file_path)
    else:
        pages = extract_text_from_txt(file_path)

    # Chunk text
    chunks = chunk_text(pages, chunk_size=Config.CHUNK_SIZE, overlap=Config.CHUNK_OVERLAP)

    doc_id = str(uuid.uuid4())
    file_size = os.path.getsize(file_path)

    # Insert document
    conn.execute(
        "INSERT INTO documents (id, filename, file_hash, file_type, chunk_count, file_size) VALUES (?, ?, ?, ?, ?, ?)",
        (doc_id, filename, file_hash, ext, len(chunks), file_size)
    )

    # Insert chunks
    for c in chunks:
        chunk_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO document_chunks (id, document_id, filename, page, section, chunk_index, text) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (chunk_id, doc_id, filename, c["page"], c["section"], c["chunk_index"], c["text"])
        )

    conn.commit()
    conn.close()

    duration = (time.time() - start_time) * 1000
    log_execution(
        trace_id=f"ingest-{doc_id[:8]}",
        component="KnowledgeBase",
        call_type="ingest_document",
        inputs={"filename": filename, "file_size": file_size, "replace": replace_existing},
        outputs={"doc_id": doc_id, "chunk_count": len(chunks)},
        duration_ms=duration
    )

    return {
        "status": "success",
        "doc_id": doc_id,
        "filename": filename,
        "chunk_count": len(chunks),
        "message": "Document ingested successfully"
    }

def query_knowledge_base(query: str, top_k: int = 3) -> List[Dict[str, Any]]:
    """Retrieves top_k relevant chunks from SQLite knowledge base"""
    start_time = time.time()
    conn = get_db_connection()
    chunks = conn.execute("SELECT * FROM document_chunks").fetchall()
    conn.close()

    if not chunks:
        return []

    q_vec = SimpleVectorStore._tokenize(query)
    scored_chunks = []

    for c in chunks:
        c_dict = dict(c)
        c_vec = SimpleVectorStore._tokenize(c_dict["text"])
        score = SimpleVectorStore._cosine_similarity(q_vec, c_vec)
        if score > 0.05: # Relevance threshold
            scored_chunks.append({
                "chunk_id": c_dict["id"],
                "document_id": c_dict["document_id"],
                "filename": c_dict["filename"],
                "page": c_dict["page"],
                "section": c_dict["section"],
                "chunk_index": c_dict["chunk_index"],
                "text": c_dict["text"],
                "score": round(score, 4)
            })

    scored_chunks.sort(key=lambda x: x["score"], reverse=True)
    results = scored_chunks[:top_k]

    duration = (time.time() - start_time) * 1000
    log_execution(
        trace_id=f"rag-{uuid.uuid4().hex[:8]}",
        component="RAG",
        call_type="query_knowledge_base",
        inputs={"query": query, "top_k": top_k},
        outputs={"matched_count": len(results), "results": results},
        duration_ms=duration
    )

    return results
