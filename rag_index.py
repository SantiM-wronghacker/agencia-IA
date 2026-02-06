from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

KB_DIR = Path("kb")
DB_DIR = Path("memory_db")
COLLECTION_NAME = "kb_store"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(DB_DIR),
    settings=Settings(anonymized_telemetry=False)
)
col = client.get_or_create_collection(COLLECTION_NAME)

def chunk_text(text: str, chunk_size=900, overlap=120):
    chunks = []
    i = 0
    while i < len(text):
        chunks.append(text[i:i+chunk_size])
        i += chunk_size - overlap
    return chunks

def main():
    files = list(KB_DIR.glob("*"))
    if not files:
        print("No hay archivos en kb/. Agrega algo y vuelve a correr.")
        return

    ids, docs, metas, embs = [], [], [], []
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="ignore")
        chunks = chunk_text(txt)
        for j, ch in enumerate(chunks):
            ids.append(f"{f.name}__{j}")
            docs.append(ch)
            metas.append({"source": f.name, "chunk": j})
            embs.append(model.encode(ch).tolist())

    # re-index limpio (opcional): borra y recrea
    try:
        client.delete_collection(COLLECTION_NAME)
        col2 = client.get_or_create_collection(COLLECTION_NAME)
    except Exception:
        col2 = col

    col2.add(ids=ids, documents=docs, metadatas=metas, embeddings=embs)
    print(f"✅ Indexados {len(ids)} chunks desde {len(files)} archivos en kb/")

if __name__ == "__main__":
    main()
