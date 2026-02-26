"""
AREA: CEREBRO
DESCRIPCION: Agente de búsqueda de información en una base de conocimiento
TECNOLOGIA: chromadb, sentence_transformers
"""
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from pathlib import Path
import sys
import time
import json

DB_DIR = Path(sys.argv[2]) if len(sys.argv) > 2 else Path("memory_db")
COLLECTION_NAME = sys.argv[3] if len(sys.argv) > 3 else "kb_store"

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(
    path=str(DB_DIR),
    settings=Settings(anonymized_telemetry=False)
)
col = client.get_or_create_collection(COLLECTION_NAME)

def search(query: str, k=3):
    try:
        q_emb = model.encode(query).tolist()
        res = col.query(query_embeddings=[q_emb], n_results=k)
        docs = res["documents"][0]
        metas = res["metadatas"][0]

        out = []
        for d, m in zip(docs, metas):
            out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
        return "\n\n---\n\n".join(out)
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python rag_query.py <pregunta> [db_dir] [collection_name]")
        pregunta = "¿Cuál es el propósito de la vida?"
    else:
        pregunta = sys.argv[1]
    result = search(pregunta)
    if len(result.split('\n')) < 20:
        result += "\n\nInformación adicional:\n"
        result += "Base de conocimiento: " + str(DB_DIR) + "\n"
        result += "Colección: " + COLLECTION_NAME + "\n"
        result += "Número de resultados: 3\n"
        result += "Modelo de lenguaje: all-MiniLM-L6-v2\n"
    print("\n" + result + "\n")
    print("Resumen ejecutivo: Se ha realizado una búsqueda en la base de conocimiento con la pregunta '" + pregunta + "'.")
    time.sleep(2)