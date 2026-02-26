"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente con memoria (RAG) que responde preguntas utilizando un modelo de lenguaje y una base de conocimiento.
TECNOLOGÍA: Python, Groq, Chroma
"""


from llm_router import completar

def _groq_compat_create(**kwargs):
    """Compatibilidad con llamadas antiguas a client.chat.completions.create"""
    messages = kwargs.get('messages', [])
    temperatura = kwargs.get('temperature', 0.5)
    max_tokens = kwargs.get('max_tokens', 1000)

    class _Resp:
        class _Choice:
            class _Msg:
                content = ""
            message = _Msg()
        choices = [_Choice()]

    resultado = completar(messages, temperatura=temperatura, max_tokens=max_tokens)
    resp = _Resp()
    resp.choices[0].message.content = resultado or ""
    return resp

from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import sys
import time

MODEL = "llama-3.3-70b"
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
    print("Agente con memoria (RAG) listo.")
    index_kb()

    api_key = "Tu_API_Key_Aqui"  # Reemplaza con tu API Key
    pregunta = "¿Cuál es el propósito de este agente?"
    if len(sys.argv) > 1:
        pregunta = sys.argv[1]

    context = query_kb(pregunta)

    prompt = f"""Usa esta información para responder:

{context}

Pregunta: {pregunta}
"""

    r = groq.Chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "Eres un asistente empresarial preciso."},
            {"role": "user", "content": prompt},
        ],
        api_key=api_key,
    )

    print("\nAgente:", r["message"]["content"].strip(), "\n")

if __name__ == "__main__":
    main()