"""
ÁREA: CEREBRO
DESCRIPCIÓN: Gestiona la memoria de conversaciones y actualiza resúmenes.
TECNOLOGÍA: Python, json, requests, Groq
"""
import json
from pathlib import Path
import requests
import sys
import time

MODEL = "groq"
API_KEY = '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'
BASE_URL = "https://api.groq.com"

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

def groq(system: str, user: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ]
    }
    response = requests.post(BASE_URL + "/chat", headers=headers, json=data)
    return response.json()["message"]["content"].strip()

def update_summary(old_summary: str, new_lines: str) -> str:
    prompt = f"""Resumen anterior:
{old_summary}

Nuevos mensajes (recientes):
{new_lines}
"""
    return groq(SUMMARY_SYSTEM, prompt)

def add_recent(state, role, content, max_recent=8):
    state["recent"].append({"role": role, "content": content})
    state["recent"] = state["recent"][-(max_recent * 2):]
    return state

if __name__ == "__main__":
    state = load_state()
    if len(sys.argv) > 1:
        user = sys.argv[1]
    else:
        user = "Hola"
    print(f"Memory manager listo. Usuario: {user}.\n")

    state = add_recent(state, "user", user)

    assistant = "(respuesta simulada)"
    state = add_recent(state, "assistant", assistant)

    recent_text = "\n".join([f"{m['role']}: {m['content']}" for m in state["recent"][-6:]])
    state["summary"] = update_summary(state["summary"], recent_text)
    save_state(state)

    time.sleep(2)
    print("\n✅ Resumen actualizado en runs/state.json\n")
    print("Resumen:")
    print(state["summary"])