"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente de planificación y ejecución de tareas
TECNOLOGÍA: Python, Groq
"""


from llm_router import completar

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

from datetime import datetime
from pathlib import Path
import sys
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

API_KEY = "tu_api_key_aquí"
RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)
MODEL = "groq:base"

def save_run(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    filename = RUNS_DIR / f"{ts}_{safe_title or 'run'}.md"
    filename.write_text(content, encoding="utf-8")
    return str(filename)

def chat(model: str, system: str, user: str) -> str:
    r = groq.chat(
        api_key=API_KEY,
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    time.sleep(2)
    return r["message"]["content"].strip()

SYSTEM = """Eres un planificador y ejecutor. Convierte la petición en un plan accionable y produce un primer entregable real en texto.
Si faltan datos, asume lo mínimo razonable y marca TODO supuesto.
Entrega en Markdown, con secciones y checklist.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) Lista de entregables
4) Riesgos y supuestos (breve)
Sé concreto.
"""

def main():
    if len(sys.argv) < 2:
        task = "Planificar y ejecutar una tarea"
    else:
        task = sys.argv[1]

    print("Equipo de agentes (Planificador + Ejecutor). Tarea:", task, "\n")

    result = chat(MODEL, SYSTEM, task)

    report = f"# Tarea\n{task}\n\n# Resultado\n{result}\n"
    path = save_run("equipo_agentes", report)

    print("\n Listo. Guardé el resultado en:", path, "\n")

if __name__ == "__main__":
    main()