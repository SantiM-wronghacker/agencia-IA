# ARCHIVO: rag_pro.py
# AREA: CEREBRO
# DESCRIPCION: Agente de búsqueda en base de conocimiento
# TECNOLOGIA: Python, ChromaDB, SentenceTransformer

import logging
import sys
from pathlib import Path
import json
from datetime import datetime

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

logger = logging.getLogger(__name__)

def _get_collection(db_dir: Path, collection_name: str):
    try:
        client = chromadb.PersistentClient(
            path=str(db_dir),
            settings=Settings(anonymized_telemetry=False),
        )
        return client.get_or_create_collection(collection_name)
    except Exception as e:
        logger.error(f"Error al obtener la colección: {e}")
        return None

def search_kb(query: str, k: int = 3, db_dir: Path = Path(sys.argv[1]), collection_name: str = sys.argv[2]) -> str:
    try:
        col = _get_collection(db_dir, collection_name)
        if col is None:
            return "No se pudo obtener la colección."
        
        _model = SentenceTransformer(sys.argv[3])
        q_emb = _model.encode(query).tolist()
        res = col.query(query_embeddings=[q_emb], n_results=k)

        docs = res["documents"][0]
        metas = res["metadatas"][0]

        out = []
        for d, m in zip(docs, metas):
            out.append(f"[Fuente: {m.get('source')} | chunk={m.get('chunk')}]\n{d}")
        
        if len(out) < 20:
            out.append(f"Fecha de búsqueda: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            out.append(f"Número de resultados: {len(out)}")
            out.append(f"Consulta: {query}")
            out.append(f"Base de datos: {db_dir}")
            out.append(f"Collection name: {collection_name}")
        
        resultado = "\n\n---\n\n".join(out) if out else "No encontré contexto relevante en la KB."
        resumen = f"Resumen ejecutivo: Se encontraron {len(out)} resultados relevantes para la consulta '{query}' en la base de datos {db_dir} y collection {collection_name}."
        return f"{resultado}\n\n{resumen}"
    except Exception as e:
        logger.error(f"Error al buscar en la base de conocimiento: {e}")
        return "No se pudo realizar la búsqueda."

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Uso: python rag_pro.py <db_dir> <collection_name> <embedding_model>")
    else:
        print(search_kb(sys.argv[4] if len(sys.argv) > 4 else "Consulta de ejemplo"))