"""
Consolidated router for the Agencia Santi multi-agent system.

Merges functionality from:
  - agent_router.py          (basic intent classification)
  - agent_router_memory.py   (session memory)
  - agent_router_memory_pro.py (memory + RAG PRO)
  - agent_router_state_pro.py  (hybrid state-based memory)

Provides ``DynamicRouter`` — a single class that handles intent
classification, state management, handler dispatch, and optional
auto-escalation between FAST and STRONG models.
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Ensure the repository root is on sys.path so that the existing
# flat-layout modules (core, config, rag_pro, …) are importable.
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from config import (
    MODEL_FAST,
    MODEL_STRONG,
    PROJECTS_DIR,
    RUNS_DIR,
    KB_DIR,
)
from core import (
    llm,
    load_state,
    save_state,
    add_recent,
    format_recent,
    build_context_prefix,
    update_summary,
    save_md,
    SYSTEM_ROUTER,
    SYSTEM_CHAT,
    SYSTEM_PLANNER,
    SYSTEM_EXEC,
)

logger = logging.getLogger(__name__)

# Re-export commonly used symbols so callers can do:
#   from src.agencia.core.router import load_state, save_state, ...
__all__ = [
    "DynamicRouter",
    "load_state",
    "save_state",
    "add_recent",
    "format_recent",
    "build_context_prefix",
    "update_summary",
    "save_md",
    "ensure_project",
    "route_intent",
    "handle_chat",
    "handle_save",
    "handle_task",
    "handle_rag",
    "needs_escalation",
]


# ─── Auto-escalation heuristic ────────────────────────────────────────
def needs_escalation(answer: str, route: str = "CHAT") -> bool:
    """Decide whether to retry with MODEL_STRONG."""
    a = (answer or "").strip().lower()
    if not a:
        return True

    red_flags = [
        "no sé",
        "no estoy seguro",
        "no tengo información",
        "no puedo",
        "no cuento con",
        "no encontré",
        "no aparece",
        "no está en el contexto",
    ]
    if any(flag in a for flag in red_flags):
        return True

    if route in ("TASK", "RAG") and len(a) < 60:
        return True

    return False


# ─── Project helpers ──────────────────────────────────────────────────
DEFAULT_AGENTS = [
    {"id": "chat", "name": "Chat", "enabled": True},
    {"id": "rag", "name": "RAG PRO", "enabled": True},
    {"id": "save", "name": "Save (notes)", "enabled": True},
    {"id": "task", "name": "Task (Planner+Executor)", "enabled": True},
    {"id": "router", "name": "Router", "enabled": True},
]


def ensure_project(company: str, project: str) -> Path:
    """Create project directory structure and initialise state + config."""
    p = PROJECTS_DIR / company / project
    (p / "kb").mkdir(parents=True, exist_ok=True)
    (p / "runs").mkdir(parents=True, exist_ok=True)
    (p / "memory_db").mkdir(parents=True, exist_ok=True)

    state_file = p / "runs" / "state.json"
    if not state_file.exists():
        save_state({"summary": "", "recent": []}, state_file=state_file)

    cfg = p / "config.json"
    if not cfg.exists():
        cfg.write_text(
            json.dumps({"agents": DEFAULT_AGENTS}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return p


# ─── Standalone routing functions ─────────────────────────────────────
def route_intent(state: dict, user_text: str) -> str:
    """Classify user intent into CHAT / SAVE / TASK / RAG."""
    prompt = (
        f"{build_context_prefix(state)}\n"
        f"RECENTE:\n{format_recent(state, 6)}\n\n"
        f"MENSAJE:\n{user_text}"
    )
    out = llm(SYSTEM_ROUTER, prompt, model=MODEL_FAST).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"


def handle_chat(state: dict, user_text: str) -> str:
    prompt = (
        f"{build_context_prefix(state)}\n"
        f"RECENTE:\n{format_recent(state, 10)}\n\n"
        f"MENSAJE:\n{user_text}"
    )
    return llm(SYSTEM_CHAT, prompt, model=MODEL_FAST)


def handle_save(project_path: Path, user_text: str) -> str:
    runs_dir = project_path / "runs"
    md_content = f"# Nota\n\n{user_text}\n"
    path = save_md("nota", md_content, runs_dir=runs_dir)
    return f"Guardado en: {path}"


def handle_task(project_path: Path, state: dict, user_text: str) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)
    planner_prompt = (
        f"{prefix}\nCONVERSACIÓN RECIENTE:\n{recent}\n\nTAREA:\n{user_text}"
    )
    plan = llm(SYSTEM_PLANNER, planner_prompt, model=MODEL_STRONG)
    deliverable = llm(
        SYSTEM_EXEC,
        f"Petición:\n{user_text}\n\nPlan:\n{plan}",
        model=MODEL_STRONG,
    )
    report = (
        f"# Tarea\n{user_text}\n\n"
        f"# Memoria (resumen)\n{state.get('summary', '')}\n\n"
        f"# Plan\n{plan}\n\n"
        f"# Entregable\n{deliverable}\n"
    )
    runs_dir = project_path / "runs"
    path = save_md("tarea_proyecto", report, runs_dir=runs_dir)
    return f"TASK completado y guardado en: {path}"


def handle_rag(project_path: Path, state: dict, user_text: str) -> str:
    try:
        from rag_pro import search_kb

        db_dir = project_path / "memory_db"
        context = search_kb(user_text, k=3, db_dir=db_dir)
    except Exception:
        context = "No hay contexto disponible"

    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)
    prompt = (
        f"{prefix}\n"
        f"CONVERSACIÓN RECIENTE:\n{recent}\n\n"
        f"INSTRUCCIÓN:\nResponde usando SOLO el contexto (KB). "
        f"Si no está en el contexto, dilo.\n\n"
        f"CONTEXTO (KB):\n{context}\n\n"
        f"PREGUNTA:\n{user_text}"
    )
    return llm(SYSTEM_CHAT, prompt, model=MODEL_FAST)


# ─── DynamicRouter class ─────────────────────────────────────────────
class DynamicRouter:
    """Unified router combining basic, memory, memory-pro, and state-pro
    routing patterns into a single, configurable class.

    Usage::

        router = DynamicRouter()
        state = router.load_state(project_path)
        route = router.route_intent(state, user_text)
        result = router.dispatch(route, project_path, state, user_text)
    """

    ROUTES = frozenset({"CHAT", "SAVE", "TASK", "RAG"})

    def __init__(self, auto_escalate: bool = False):
        self.auto_escalate = auto_escalate

    # ── State helpers ─────────────────────────────────────────────
    @staticmethod
    def load_state(project_path: Path) -> dict:
        return load_state(state_file=project_path / "runs" / "state.json")

    @staticmethod
    def save_state(project_path: Path, state: dict) -> None:
        save_state(state, state_file=project_path / "runs" / "state.json")

    # ── Intent classification ─────────────────────────────────────
    def route_intent(self, state: dict, user_text: str) -> str:
        return route_intent(state, user_text)

    # ── Handler dispatch ──────────────────────────────────────────
    def dispatch(
        self,
        route: str,
        project_path: Path,
        state: dict,
        user_text: str,
    ) -> str:
        handlers = {
            "SAVE": lambda: handle_save(project_path, user_text),
            "TASK": lambda: handle_task(project_path, state, user_text),
            "RAG": lambda: handle_rag(project_path, state, user_text),
            "CHAT": lambda: handle_chat(state, user_text),
        }
        handler = handlers.get(route, handlers["CHAT"])
        answer = handler()

        if self.auto_escalate and needs_escalation(answer, route=route):
            logger.info("Escalating from %s to %s", MODEL_FAST, MODEL_STRONG)
            # Re-run with the strong model via direct llm call
            prefix = build_context_prefix(state)
            recent = format_recent(state, n_msgs=10)
            prompt = (
                f"{prefix}\nRECENTE:\n{recent}\n\nMENSAJE:\n{user_text}"
            )
            answer = llm(SYSTEM_CHAT, prompt, model=MODEL_STRONG)

        return answer
