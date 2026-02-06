import json
from pathlib import Path
import ollama

MODEL = "llama3:8b"

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

STATE_FILE = RUNS_DIR / "state.json"

SUMMARY_SYSTEM = """Eres un compresor de memoria.
Actualiza un resumen vivo de la conversación.
Reglas:
- Mantén el resumen en 10-20 líneas.
- Conserva: objetivos, decisiones, preferencias, datos (precios, nombres), pendientes.
- Elimina: charla repetitiva.
Devuelve SOLO el resumen actualizado.
"""

def load_state():
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"summary": "", "recent": []}

def save_state(state):
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

def llm(system: str, user: str) -> str:
    r = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return r["message"]["content"].strip()

def update_summary(old_summary: str, new_lines: str) -> str:
    prompt = f"""Resumen anterior:
{old_summary}

Nuevos mensajes (recientes):
{new_lines}
"""
    return llm(SUMMARY_SYSTEM, prompt)

def add_recent(state, role, content, max_recent=8):
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(max_recent * 2):]
    return state

if __name__ == "__main__":
    state = load_state()
    print("Memory manager listo. Escribe 'salir'.\n")

    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        state = add_recent(state, "user", user)

        # simulamos respuesta “assistant” para probar resumen
        # (en tu router real, en vez de esto, metes la respuesta real)
        assistant = "(respuesta simulada)"
        state = add_recent(state, "assistant", assistant)

        recent_text = "\n".join([f"{m['role']}: {m['content']}" for m in state["recent"][-6:]])
        state["summary"] = update_summary(state["summary"], recent_text)
        save_state(state)

        print("\n✅ Resumen actualizado en runs/state.json\n")
