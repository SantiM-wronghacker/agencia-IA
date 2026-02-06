import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path

DB_DIR = Path("memory_db")
COLLECTION_NAME = "kb_store"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(DB_DIR),
    settings=Settings(anonymized_telemetry=False)
)
col = client.get_or_create_collection(COLLECTION_NAME)

def search(query: str, k=3):
    q_emb = model.encode(query).tolist()
    res = col.query(query_embeddings=[q_emb], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]

    out = []
    for d, m in zip(docs, metas):
        out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
    return "\n\n---\n\n".join(out)

if __name__ == "__main__":
    while True:
        q = input("Pregunta (o salir): ").strip()
        if q.lower() in ("salir", "exit", "quit"):
            break
        print("\n" + search(q) + "\n")
