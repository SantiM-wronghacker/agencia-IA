import json
from pathlib import Path
from datetime import datetime
import ollama

# Modelos
MODEL_FAST = "llama3:8b"
MODEL_STRONG = "gpt-oss:20b"

# Directorios
BASE_DIR = Path(".")
PROJECTS_DIR = BASE_DIR / "projects"
PROJECTS_DIR.mkdir(exist_ok=True)

def ensure_project(company: str, project: str) -> Path:
    p = PROJECTS_DIR / company / project
    (p / "kb").mkdir(parents=True, exist_ok=True)
    (p / "runs").mkdir(parents=True, exist_ok=True)
    (p / "memory_db").mkdir(parents=True, exist_ok=True)
    state = p / "runs" / "state.json"
    if not state.exists():
        state.write_text(json.dumps({"summary": "", "recent": []}, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def load_state(project_path: Path):
    f = project_path / "runs" / "state.json"
    return json.loads(f.read_text(encoding="utf-8"))

def save_state(project_path: Path, state):
    f = project_path / "runs" / "state.json"
    f.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def add_recent(state, role, content, max_recent_turns=10):
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(max_recent_turns * 2):]
    return state

def format_recent(state, n_msgs=8):
    msgs = state["recent"][-n_msgs:]
    return "\n".join([f"{m['role']}: {m['content']}" for m in msgs])

def llm(system: str, user: str, model: str):
    r = ollama.chat(model=model, messages=[
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ])
    return r["message"]["content"].strip()

SYSTEM_ROUTER = """Devuelve SOLO una palabra: CHAT, SAVE, TASK, RAG.
SAVE solo si empieza con 'guardar:'.
TASK si pide plan/estrategia/checklist/propuesta/documento.
RAG si pide info basada en KB.
Si no: CHAT.
"""

SYSTEM_CHAT = "Eres un asistente útil, directo y práctico."
SUMMARY_SYSTEM = """Actualiza un resumen vivo (10-20 líneas). Devuelve SOLO el resumen."""

def build_context_prefix(state):
    s = state.get("summary", "").strip()
    return f"MEMORIA:\n{s}\n" if s else ""

def route_intent(state, user_text) -> str:
    prompt = f"{build_context_prefix(state)}\nRECENTE:\n{format_recent(state,6)}\n\nMENSAJE:\n{user_text}"
    out = llm(SYSTEM_ROUTER, prompt, model=MODEL_FAST).upper().split()[0]
    return out if out in ("CHAT","SAVE","TASK","RAG") else "CHAT"

def update_summary(state):
    prompt = f"Resumen anterior:\n{state.get('summary','')}\n\nMensajes recientes:\n{format_recent(state,8)}"
    state["summary"] = llm(SUMMARY_SYSTEM, prompt, model=MODEL_FAST)
    return state

# Stubs básicos para compatibilidad con api.py
def handle_chat(state, user_text: str) -> str:
    prompt = f"{build_context_prefix(state)}\nRECENTE:\n{format_recent(state,10)}\n\nMENSAJE:\n{user_text}"
    return llm(SYSTEM_CHAT, prompt, model=MODEL_FAST)

def handle_save(project_path: Path, user_text: str) -> str:
    runs_dir = project_path / "runs"
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = runs_dir / f"{ts}_nota.md"
    path.write_text(user_text, encoding="utf-8")
    return f"✅ Guardado en: {path}"

def handle_task(project_path: Path, state, user_text: str) -> str:
    # Por ahora devolvemos un placeholder (luego conectamos planner/executor)
    return f"✅ TASK recibido: {user_text}"

def handle_rag(project_path: Path, state, user_text: str) -> str:
    return "RAG aún no conectado en este archivo mínimo."
