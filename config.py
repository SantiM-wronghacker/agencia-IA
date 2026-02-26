"""
Centralized configuration for the multi-agent system.
Reads from environment variables (or .env file) with sensible defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# --- Directories ---
BASE_DIR = Path(os.getenv("AGENTS_BASE_DIR", "."))
RUNS_DIR = BASE_DIR / "runs"
KB_DIR = BASE_DIR / "kb"
MEMORY_DB_DIR = BASE_DIR / "memory_db"
PROJECTS_DIR = BASE_DIR / "projects"

RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

# --- Models ---
MODEL_FAST = os.getenv("MODEL_FAST", "llama3:8b")
MODEL_STRONG = os.getenv("MODEL_STRONG", "gpt-oss:20b")

# --- Ollama ---
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
OLLAMA_TIMEOUT = int(os.getenv("OLLAMA_TIMEOUT", "120"))

# --- Memory ---
MAX_RECENT_TURNS = int(os.getenv("MAX_RECENT_TURNS", "10"))
STATE_FILE = RUNS_DIR / "state.json"

# --- RAG ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "kb_store")
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "900"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))

# --- API ---
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))
