import ollama
from datetime import datetime
from pathlib import Path

MODEL = "llama3:8b"
RUNS_DIR = Path("runs")
RUNS_DIR.mkdir(exist_ok=True)

SYSTEM = """Eres un asistente útil y directo.
Si el usuario te pide guardar algo, crea una nota clara y estructurada.
"""

def save_note(title: str, content: str) -> str:
    ts = datetime.now().strftime("%Y%m%d-%H%M%S")
    safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "-", "_")).strip().replace(" ", "_")
    filename = RUNS_DIR / f"{ts}_{safe_title or 'nota'}.md"
    filename.write_text(content, encoding="utf-8")
    return str(filename)

def main():
    print("Agente con archivos listo.")
    print("Formato para guardar:")
    print("  guardar: Titulo | Texto")
    print("Escribe 'salir' para terminar.\n")

    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        if user.lower().startswith("guardar:"):
            payload = user[len("guardar:"):].strip()
            if "|" not in payload:
                print("Formato correcto: guardar: Titulo | Texto\n")
                continue

            title, text = [x.strip() for x in payload.split("|", 1)]
            md = f"# {title}\n\n{text}\n"
            path = save_note(title, md)
            print(f"✅ Guardado en: {path}\n")
            continue

        resp = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": user},
            ],
        )
        print("\nAgente:", resp["message"]["content"].strip(), "\n")

if __name__ == "__main__":
    main()
