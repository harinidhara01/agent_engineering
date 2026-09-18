import os
import time
import hashlib
import uuid
import re
import math
from typing import List, Dict, Any, Tuple
from config import Config
from database import get_db_connection, log_execution

# Try importing ChromaDB; fallback gracefully if dependencies missing
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except Exception:
    CHROMA_AVAILABLE = False

# Fallback text extraction helpers
def extract_text_from_pdf(file_path: str) -> List[Dict[str, Any]]:
    pages = []
    try:
        import pypdf
        reader = pypdf.PdfReader(file_path)
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                pages.append({"page": idx + 1, "text": text.strip()})
    except Exception as e:
        print(f"pypdf extraction error: {e}")

    # Fallback to raw text string search if pypdf is unavailable
    if not pages:
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            strings = re.findall(rb'\(([\w\s.,;:!?\'"()-]{3,})\)', content)
            text_lines = [s.decode('latin1', errors='ignore').strip() for s in strings if len(s.strip()) > 3]
            joined_text = "\n".join(text_lines)
            if len(joined_text.strip()) > 10:
                pages.append({"page": 1, "text": joined_text.strip()})
        except Exception:
            pass

    return pages if pages else [{"page": 1, "text": f"Document: {os.path.basename(file_path)}"}]

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
    hasher = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def check_duplicate_document(file_path: str) -> Tuple[bool, Dict[str, Any]]:
    file_hash = compute_file_hash(file_path)
    conn = get_db_connection()
    doc = conn.execute("SELECT * FROM documents WHERE file_hash = ?", (file_hash,)).fetchone()
    conn.close()
    if doc:
        return True, dict(doc)
    return False, {}

def chunk_text(pages: List[Dict[str, Any]], chunk_size: int = 500, overlap: int = 50) -> List[Dict[str, Any]]:
    chunks = []
    chunk_index = 0

    for page_info in pages:
        page_num = page_info["page"]
        text = page_info["text"]

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

# Try importing ChromaDB & SentenceTransformer embedding functions
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except Exception:
    CHROMA_AVAILABLE = False

# ChromaDB Vector Store Helper with Local Hugging Face Sentence Transformers Model
def get_chroma_collection():
    if not CHROMA_AVAILABLE:
        return None
    try:
        os.makedirs(Config.VECTOR_DB_PATH, exist_ok=True)
        client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
        
        # Use local HuggingFace embedding model specified in Config.EMBEDDING_MODEL
        emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=Config.EMBEDDING_MODEL
        )
        return client.get_or_create_collection(
            name="employee_policies",
            embedding_function=emb_fn
        )
    except Exception as e:
        print(f"ChromaDB SentenceTransformer init note: {e}")
        try:
            # Fallback to default ChromaDB embedding function if sentence_transformers package is missing
            client = chromadb.PersistentClient(path=Config.VECTOR_DB_PATH)
            emb_fn = embedding_functions.DefaultEmbeddingFunction()
            return client.get_or_create_collection(
                name="employee_policies",
                embedding_function=emb_fn
            )
        except Exception:
            return None

# Lightweight In-Memory / Vector Fallback Search Engine
class SimpleVectorStore:
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
    """Ingests PDF/TXT/DOCX document into SQLite DB and ChromaDB vector store"""
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
        conn.execute("DELETE FROM document_chunks WHERE document_id = ?", (existing_doc["id"],))
        conn.execute("DELETE FROM documents WHERE id = ?", (existing_doc["id"],))
        conn.commit()
        
        # Remove from ChromaDB if available
        collection = get_chroma_collection()
        if collection:
            try:
                collection.delete(where={"document_id": existing_doc["id"]})
            except Exception:
                pass

    ext = os.path.splitext(filename)[1].lower()
    if ext == ".pdf":
        pages = extract_text_from_pdf(file_path)
    elif ext == ".docx":
        pages = extract_text_from_docx(file_path)
    else:
        pages = extract_text_from_txt(file_path)

    chunks = chunk_text(pages, chunk_size=Config.CHUNK_SIZE, overlap=Config.CHUNK_OVERLAP)

    doc_id = str(uuid.uuid4())
    file_size = os.path.getsize(file_path)

    conn.execute(
        "INSERT INTO documents (id, filename, file_hash, file_type, chunk_count, file_size) VALUES (?, ?, ?, ?, ?, ?)",
        (doc_id, filename, file_hash, ext, len(chunks), file_size)
    )

    chroma_ids = []
    chroma_texts = []
    chroma_metadatas = []

    for c in chunks:
        chunk_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO document_chunks (id, document_id, filename, page, section, chunk_index, text) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (chunk_id, doc_id, filename, c["page"], c["section"], c["chunk_index"], c["text"])
        )
        chroma_ids.append(chunk_id)
        chroma_texts.append(c["text"])
        chroma_metadatas.append({
            "document_id": doc_id,
            "filename": filename,
            "page": c["page"],
            "section": c["section"],
            "chunk_id": chunk_id,
            "chunk_index": c["chunk_index"]
        })

    conn.commit()
    conn.close()

    # Store in ChromaDB vector database
    collection = get_chroma_collection()
    if collection and chroma_ids:
        try:
            collection.add(
                ids=chroma_ids,
                documents=chroma_texts,
                metadatas=chroma_metadatas
            )
        except Exception as e:
            print(f"ChromaDB insert note: {e}")

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
    """Retrieves top_k relevant policy chunks using ChromaDB vector database (with SQLite fallback)"""
    start_time = time.time()
    results = []

    # Attempt query via ChromaDB vector store
    collection = get_chroma_collection()
    if collection:
        try:
            chroma_res = collection.query(
                query_texts=[query],
                n_results=top_k
            )
            if chroma_res and chroma_res.get("documents") and len(chroma_res["documents"][0]) > 0:
                docs = chroma_res["documents"][0]
                metas = chroma_res["metadatas"][0]
                distances = chroma_res["distances"][0] if chroma_res.get("distances") else [0.1] * len(docs)
                
                for d, m, dist in zip(docs, metas, distances):
                    score = round(max(0.0, 1.0 - (dist / 2.0)), 4)
                    results.append({
                        "chunk_id": m.get("chunk_id", ""),
                        "document_id": m.get("document_id", ""),
                        "filename": m.get("filename", ""),
                        "page": m.get("page", 1),
                        "section": m.get("section", ""),
                        "chunk_index": m.get("chunk_index", 0),
                        "text": d,
                        "score": score
                    })
        except Exception as e:
            print(f"ChromaDB query note: {e}")

    # Fallback to local vector engine if ChromaDB yielded no results
    if not results:
        conn = get_db_connection()
        chunks = conn.execute("SELECT * FROM document_chunks").fetchall()
        conn.close()

        if chunks:
            q_vec = SimpleVectorStore._tokenize(query)
            scored_chunks = []
            for c in chunks:
                c_dict = dict(c)
                c_vec = SimpleVectorStore._tokenize(c_dict["text"])
                score = SimpleVectorStore._cosine_similarity(q_vec, c_vec)
                if score > 0.05:
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
