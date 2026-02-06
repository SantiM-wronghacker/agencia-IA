from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

DB_DIR = Path("memory_db")
COLLECTION_NAME = "kb_store"

_model = SentenceTransformer("all-MiniLM-L6-v2")

_client = chromadb.PersistentClient(
    path=str(DB_DIR),
    settings=Settings(anonymized_telemetry=False)
)
_col = _client.get_or_create_collection(COLLECTION_NAME)

def search_kb(query: str, k: int = 3) -> str:
    q_emb = _model.encode(query).tolist()
    res = _col.query(query_embeddings=[q_emb], n_results=k)

    docs = res["documents"][0]
    metas = res["metadatas"][0]

    out = []
    for d, m in zip(docs, metas):
        out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
    return "\n\n---\n\n".join(out) if out else "No encontré contexto relevante en la KB."
