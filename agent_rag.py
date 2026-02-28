from llm_router import completar
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions
import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

MODEL = "llama-3.3-70b"
KB_DIR = Path("kb")

client = chromadb.Client()
collection = client.get_or_create_collection("knowledge")

embed = embedding_functions.DefaultEmbeddingFunction()

def index_kb():
    try:
        for file in KB_DIR.glob("*"):
            text = file.read_text(encoding="utf-8")
            collection.add(
                documents=[text],
                ids=[file.name]
            )
        print("Base de conocimiento indexada con éxito.")
    except Exception as e:
        print(f"Error al indexar la base de conocimiento: {e}")

def query_kb(question: str):
    try:
        results = collection.query(
            query_texts=[question],
            n_results=2
        )
        docs = results["documents"][0]
        return "\n".join(docs)
    except Exception as e:
        print(f"Error al consultar la base de conocimiento: {e}")
        return ""

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

def main():
    print("Agente con memoria (RAG) listo.")
    index_kb()

    if len(sys.argv) > 1:
        pregunta = sys.argv[1]
    else:
        pregunta = "¿Cuál es el propósito de este agente?"

    context = query_kb(pregunta)

    prompt = f"""Usa esta información para responder:

{context}

Pregunta: {pregunta}
"""

    try:
        resultado = _groq_compat_create(messages=[{"role": "system", "content": prompt}])
        respuesta = resultado.choices[0].message.content
        print("Respuesta:")
        print(respuesta)
        print("\nResumen Ejecutivo:")
        print(f"Se ha respondido la pregunta '{pregunta}' utilizando la base de conocimiento y el modelo de lenguaje.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()