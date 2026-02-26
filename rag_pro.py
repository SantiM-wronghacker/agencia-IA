"""RAG search: query the ChromaDB knowledge base."""
import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from config import MEMORY_DB_DIR, COLLECTION_NAME, EMBEDDING_MODEL

logger = logging.getLogger(__name__)

_model = SentenceTransformer(EMBEDDING_MODEL)


def _get_collection(db_dir: Path = MEMORY_DB_DIR, collection_name: str = COLLECTION_NAME):
    """Return a ChromaDB collection for the given db_dir."""
    client = chromadb.PersistentClient(
        path=str(db_dir),
        settings=Settings(anonymized_telemetry=False),
    )
    return client.get_or_create_collection(collection_name)


def search_kb(query: str, k: int = 3, db_dir: Path = MEMORY_DB_DIR) -> str:
    """Search the knowledge base and return formatted context."""
    col = _get_collection(db_dir)
    q_emb = _model.encode(query).tolist()
    res = col.query(query_embeddings=[q_emb], n_results=k)

    docs = res["documents"][0]
    metas = res["metadatas"][0]

    out = []
    for d, m in zip(docs, metas):
        out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
    return "\n\n---\n\n".join(out) if out else "No encontré contexto relevante en la KB."
