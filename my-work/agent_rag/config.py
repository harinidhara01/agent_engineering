import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

class Config:
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")
    EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, os.environ.get("VECTOR_DB_PATH", "database/vector_db"))
    DB_PATH = os.path.join(BASE_DIR, "database", "app.db")
    LOGS_PATH = os.path.join(BASE_DIR, "database", "logs.json")
    DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
    TOP_K = int(os.environ.get("TOP_K", 3))
    CHUNK_SIZE = int(os.environ.get("CHUNK_SIZE", 500))
    CHUNK_OVERLAP = int(os.environ.get("CHUNK_OVERLAP", 50))
