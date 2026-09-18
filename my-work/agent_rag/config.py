import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Force load .env from agent_rag directory, overriding any parent env variables
env_path = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=env_path, override=True)

class Config:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    VECTOR_DB_PATH = os.path.join(BASE_DIR, os.getenv("VECTOR_DB_PATH", "database/vector_db"))
    DB_PATH = os.path.join(BASE_DIR, "database", "app.db")
    LOGS_PATH = os.path.join(BASE_DIR, "database", "logs.json")
    DOCUMENTS_DIR = os.path.join(BASE_DIR, "documents")
    TOP_K = int(os.getenv("TOP_K", "3"))
    CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
    CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
