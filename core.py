"""
Core shared utilities for the multi-agent system.
Extracted from agent_router_state_autoscale.py, agent_router_projects.py,
agent_router_state_pro.py, memory_manager.py to eliminate duplication.
"""
import json
import logging
import ollama
from datetime import datetime
from pathlib import Path

from config import MODEL_FAST, RUNS_DIR, STATE_FILE, MAX_RECENT_TURNS

logger = logging.getLogger(__name__)

# =========================
# System Prompts (shared)
# =========================
SYSTEM_ROUTER = """Eres un Router (director) de un sistema de agentes.
Clasifica la intención en UNA ruta:

- CHAT: conversación o pregunta simple
- SAVE: guardar nota/idea
- TASK: plan + entregable
- RAG: responder usando kb/ (memoria documental)

Devuelve SOLO una palabra: CHAT, SAVE, TASK o RAG.
Reglas:
- Si menciona "guardar", "anotar", "nota", "guardar:" => SAVE
- Si pide plan, estrategia, checklist, pasos, propuesta, documento => TASK
- Si pregunta precios/políticas/procesos internos => RAG
- Si no estás seguro => CHAT
"""

SYSTEM_CHAT = "Eres un asistente útil, directo y práctico."

SYSTEM_PLANNER = """Eres un Planner senior. Convierte la petición en un plan accionable.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) Entregables
4) Riesgos y supuestos (breve)
"""

SYSTEM_EXEC = """Eres un Executor senior. Toma la petición y el plan y genera un primer entregable real.
Entrega en Markdown con checklist. Marca supuestos si faltan datos.
"""

SUMMARY_SYSTEM = """Eres un compresor de memoria.
Actualiza un resumen vivo de la conversación.
Reglas:
- Mantén el resumen en 10-20 líneas máximo.
- Conserva: objetivos, decisiones, preferencias, datos, pendientes.
- Elimina: repetición y relleno.
Devuelve SOLO el resumen actualizado.
"""


# =========================
# LLM call
# =========================
def llm(system: str, user: str, model: str = MODEL_FAST) -> str:
    """Call Ollama with a system/user message pair. Returns stripped content."""
    try:
        r = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return r["message"]["content"].strip()
    except Exception:
        logger.exception("Ollama call failed (model=%s)", model)
        raise


# =========================
# State management
# =========================
def load_state(state_file: Path = STATE_FILE) -> dict:
    """Load conversation state from JSON file."""
    if state_file.exists():
        try:
            return json.loads(state_file.read_text(encoding="utf-8"))
        except Exception:
            logger.warning("Corrupt state file %s, resetting", state_file)
    return {"summary": "", "recent": []}


def save_state(state: dict, state_file: Path = STATE_FILE) -> None:
    """Persist conversation state to JSON file."""
    state_file.write_text(
        json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def add_recent(state: dict, role: str, content: str,
               max_recent_turns: int = MAX_RECENT_TURNS) -> dict:
    """Append a message and trim to the recent window."""
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(max_recent_turns * 2):]
    return state


def format_recent(state: dict, n_msgs: int = 8) -> str:
    """Format the last n messages as 'role: content' lines."""
    msgs = state["recent"][-n_msgs:]
    return "\n".join(f"{m['role']}: {m['content']}" for m in msgs)


def build_context_prefix(state: dict) -> str:
    """Build a memory summary prefix for prompts."""
    summary = state.get("summary", "").strip()
    return f"MEMORIA (resumen):\n{summary}\n" if summary else ""


def update_summary(state: dict, model: str = MODEL_FAST) -> dict:
    """Compress recent messages into the running summary."""
    recent_text = format_recent(state, n_msgs=8)
    prompt = f"""Resumen anterior:
{state.get("summary", "")}

Nuevos mensajes recientes:
{recent_text}
"""
    state["summary"] = llm(SUMMARY_SYSTEM, prompt, model=model)
    return state


# =========================
# File output
# =========================
def save_md(title: str, content: str, runs_dir: Path = RUNS_DIR) -> str:
    """Save a Markdown deliverable to the runs directory. Returns the path string."""
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = "".join(
        c for c in title if c.isalnum() or c in (" ", "-", "_")
    ).strip().replace(" ", "_")
    path = runs_dir / f"{ts}_{safe or 'run'}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)
