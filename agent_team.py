import ollama
from datetime import datetime
from pathlib import Path

RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

PLANNER_MODEL = "llama3:8b"
EXEC_MODEL = "llama3:8b"   # luego lo puedes subir a gpt-oss:20b

def save_run(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    filename = RUNS_DIR / f"{ts}_{safe_title or 'run'}.md"
    filename.write_text(content, encoding="utf-8")
    return str(filename)

def chat(model: str, system: str, user: str) -> str:
    r = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    return r["message"]["content"].strip()

PLANNER_SYSTEM = """Eres un Planner. Convierte la petición en un plan accionable.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) Lista de entregables
4) Riesgos y supuestos (breve)
Sé concreto.
"""

EXEC_SYSTEM = """Eres un Executor. Tomas el plan y produces un primer entregable real en texto.
Si faltan datos, asume lo mínimo razonable y marca TODO supuesto.
Entrega en Markdown, con secciones y checklist.
"""

def main():
    print("Equipo de agentes (Planner + Executor). Escribe 'salir' para terminar.\n")

    while True:
        task = input("Tarea: ").strip()
        if task.lower() in ("salir", "exit", "quit"):
            break

        plan = chat(PLANNER_MODEL, PLANNER_SYSTEM, task)
        deliverable = chat(EXEC_MODEL, EXEC_SYSTEM, f"Petición:\n{task}\n\nPlan:\n{plan}")

        report = f"# Tarea\n{task}\n\n# Plan (Planner)\n{plan}\n\n# Entregable (Executor)\n{deliverable}\n"
        path = save_run("equipo_agentes", report)

        print("\n✅ Listo. Guardé el resultado en:", path, "\n")

if __name__ == "__main__":
    main()
