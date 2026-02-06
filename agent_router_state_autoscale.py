import json
import ollama
from datetime import datetime
from pathlib import Path
from rag_pro import search_kb

# =========================
# Config: modelos
# =========================
MODEL_FAST = "llama3:8b"
MODEL_STRONG = "gpt-oss:20b"

RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

STATE_FILE = RUNS_DIR / "state.json"
MAX_RECENT_TURNS = 10

# =========================
# Prompts
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
# Helpers
# =========================
def llm(system: str, user: str, model: str) -> str:
    r = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return r["message"]["content"].strip()

def save_md(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    path = RUNS_DIR / f"{ts}_{safe or 'run'}.md"
    path.write_text(content, encoding="utf-8")
    return str(path)

# =========================
# State (summary + recent)
# =========================
def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"summary": "", "recent": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def add_recent(state, role, content):
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(MAX_RECENT_TURNS * 2):]
    return state

def format_recent(state, n_msgs=8):
    msgs = state["recent"][-n_msgs:]
    return "\n".join([f"{m['role']}: {m['content']}" for m in msgs])

def build_context_prefix(state) -> str:
    summary = state.get("summary", "").strip()
    return f"MEMORIA (resumen):\n{summary}\n" if summary else ""

def update_summary(state):
    recent_text = format_recent(state, n_msgs=8)
    prompt = f"""Resumen anterior:
{state.get("summary","")}

Nuevos mensajes recientes:
{recent_text}
"""
    state["summary"] = llm(SUMMARY_SYSTEM, prompt, model=MODEL_FAST)
    return state

def reset_state():
    s = {"summary": "", "recent": []}
    save_state(s)
    return s

# =========================
# Auto-escalado
# =========================
def needs_escalation(answer: str) -> bool:
    """Heurística simple para reintentar con el modelo fuerte."""
    a = (answer or "").strip().lower()
    if not a:
        return True

    red_flags = [
        "no sé", "no estoy seguro", "no tengo información", "no puedo",
        "no cuento con", "no encontré", "no aparece", "no está en el contexto"
    ]
    if any(x in a for x in red_flags):
        return True

    # si es demasiado corto, suele ser mala calidad en tareas de contenido
    if len(a) < 60:
        return True

    return False

# =========================
# Router + Handlers
# =========================
def route_intent(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=6)
    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE ACTUAL:
{user_text}
"""
    out = llm(SYSTEM_ROUTER, prompt, model=MODEL_FAST).upper().split()[0]
    return out if out in ("CHAT", "SAVE", "TASK", "RAG") else "CHAT"

def handle_save(user_text) -> str:
    if user_text.lower().startswith("guardar:") and "|" in user_text:
        payload = user_text[len("guardar:"):].strip()
        title, text = [x.strip() for x in payload.split("|", 1)]
    else:
        title, text = "nota", user_text

    md = f"# {title}\n\n{text}\n"
    path = save_md(title, md)
    return f"✅ Guardado en: {path}"

def handle_task(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)

    planner_prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

TAREA:
{user_text}
"""
    # TASK siempre STRONG
    plan = llm(SYSTEM_PLANNER, planner_prompt, model=MODEL_STRONG)
    deliverable = llm(SYSTEM_EXEC, f"Petición:\n{user_text}\n\nPlan:\n{plan}", model=MODEL_STRONG)

    report = f"# Tarea\n{user_text}\n\n# Memoria (resumen)\n{state.get('summary','')}\n\n# Plan\n{plan}\n\n# Entregable\n{deliverable}\n"
    path = save_md("tarea_autoscale", report)
    return f"✅ TASK (20B) listo y guardado en: {path}"

def answer_with_autoscale(system: str, prompt: str, allow_strong_retry: bool = True) -> str:
    ans_fast = llm(system, prompt, model=MODEL_FAST)
    if allow_strong_retry and needs_escalation(ans_fast):
        ans_strong = llm(system, prompt, model=MODEL_STRONG)
        # si el strong también es malo, regresamos el fast (o strong si tiene algo)
        return ans_strong.strip() or ans_fast
    return ans_fast

def handle_rag(state, user_text) -> str:
    context = search_kb(user_text, k=3)
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=8)

    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

INSTRUCCIÓN:
Responde usando SOLO el contexto (KB). Si no está en el contexto, dilo.

CONTEXTO (KB):
{context}

PREGUNTA:
{user_text}
"""
    # En RAG normalmente basta FAST; activamos retry solo si sale flojo.
    return answer_with_autoscale(SYSTEM_CHAT, prompt, allow_strong_retry=True)

def handle_chat(state, user_text) -> str:
    prefix = build_context_prefix(state)
    recent = format_recent(state, n_msgs=10)
    prompt = f"""{prefix}
CONVERSACIÓN RECIENTE:
{recent}

MENSAJE:
{user_text}
"""
    return answer_with_autoscale(SYSTEM_CHAT, prompt, allow_strong_retry=True)

def main():
    state = load_state()
    print("Router: Memoria híbrida + RAG PRO + routing + auto-escalado (FAST→STRONG si hace falta).")
    print(f"FAST:   {MODEL_FAST}")
    print(f"STRONG: {MODEL_STRONG}")
    print("Comandos: salir | reset\n")

    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        if user.lower() == "reset":
            state = reset_state()
            print("🧹 Memoria borrada.\n")
            continue

        state = add_recent(state, "user", user)

        route = route_intent(state, user)
        print(f"\nRouter → {route}")

        if route == "SAVE":
            out = handle_save(user)
        elif route == "TASK":
            out = handle_task(state, user)
        elif route == "RAG":
            out = handle_rag(state, user)
        else:
            out = handle_chat(state, user)

        state = add_recent(state, "assistant", out)
        state = update_summary(state)
        save_state(state)

        print("\nAgente:", out, "\n")

if __name__ == "__main__":
    main()

