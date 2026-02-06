import ollama
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

MODEL = "llama3:8b"
KB_DIR = Path("kb")

client = chromadb.Client()
collection = client.get_or_create_collection("knowledge")

embed = embedding_functions.DefaultEmbeddingFunction()

def index_kb():
    for file in KB_DIR.glob("*"):
        text = file.read_text(encoding="utf-8")
        collection.add(
            documents=[text],
            ids=[file.name]
        )

def query_kb(question: str):
    results = collection.query(
        query_texts=[question],
        n_results=2
    )
    docs = results["documents"][0]
    return "\n".join(docs)

def main():
    print("Agente con memoria (RAG) listo. Escribe 'salir'.\n")
    index_kb()

    while True:
        q = input("Tú: ").strip()
        if q.lower() in ("salir", "exit", "quit"):
            break

        context = query_kb(q)

        prompt = f"""Usa esta información para responder:

{context}

Pregunta: {q}
"""

        r = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente empresarial preciso."},
                {"role": "user", "content": prompt},
            ],
        )

        print("\nAgente:", r["message"]["content"].strip(), "\n")

if __name__ == "__main__":
    main()
