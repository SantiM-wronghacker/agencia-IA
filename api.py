from fastapi import FastAPI
from pydantic import BaseModel
from pathlib import Path
import json

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
    update_summary
)

app = FastAPI()

class ChatRequest(BaseModel):
    company: str
    project: str
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
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
        "summary": state.get("summary", "")
    }