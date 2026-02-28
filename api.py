"""FastAPI backend for the multi-agent system."""
import logging

import requests as http_requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from config import OLLAMA_BASE_URL
from logging_config import setup_logging
from agent_router_projects import (
    ensure_project,
    load_state,
    save_state,
    add_recent,
    route_intent,
    handle_chat,
    handle_task,
    handle_rag,
    handle_save,
    update_summary,
)
from rag_index import index_kb

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentes Locales API", version="0.2.0")


class ChatRequest(BaseModel):
    company: str
    project: str
    message: str


class IndexRequest(BaseModel):
    company: str
    project: str


@app.get("/health")
def health():
    """Check that Ollama is reachable."""
    try:
        r = http_requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        r.raise_for_status()
        return {"status": "ok", "ollama": "connected", "models": r.json().get("models", [])}
    except Exception as exc:
        raise HTTPException(status_code=503, detail=f"Ollama unreachable: {exc}")


@app.post("/chat")
def chat(req: ChatRequest):
    try:
        project_path = ensure_project(req.company, req.project)
        state = load_state(project_path)
        state = add_recent(state, "user", req.message)
        route = route_intent(state, req.message)

        if route == "SAVE":
            out = handle_save(project_path, req.message)
        elif route == "TASK":
            out = handle_task(project_path, state, req.message)
        elif route == "RAG":
            out = handle_rag(project_path, state, req.message)
        else:
            out = handle_chat(state, req.message)

        state = add_recent(state, "assistant", out)
        state = update_summary(state)
        save_state(project_path, state)

        return {
            "route": route,
            "response": out,
            "summary": state.get("summary", ""),
        }
    except ConnectionError:
        raise HTTPException(status_code=503, detail="Ollama is not running or unreachable")
    except Exception as exc:
        logger.exception("Error in /chat")
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/index")
def index_project(req: IndexRequest):
    """Re-index the KB for a specific project."""
    try:
        project_path = ensure_project(req.company, req.project)
        kb_dir = project_path / "kb"
        db_dir = project_path / "memory_db"
        index_kb(kb_dir, db_dir)
        return {"status": "ok", "message": f"Indexed KB for {req.company}/{req.project}"}
    except Exception as exc:
        logger.exception("Error in /index")
        raise HTTPException(status_code=500, detail=str(exc))
