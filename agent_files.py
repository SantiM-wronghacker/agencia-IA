"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente con archivos que interactúa con el usuario y guarda notas en archivos markdown.
TECNOLOGÍA: Python, Groq, Markdown
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

MODEL = "llama-3.3-70b-versatile"
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
    if len(sys.argv) < 2:
        print("Usando valores por defecto.")
        user_input = "guardar: Nota de ejemplo | Este es un ejemplo de nota."
    else:
        user_input = " ".join(sys.argv[1:])

    print("Agente con archivos listo.")
    print("Formato para guardar:")
    print("  guardar: Titulo | Texto")
    print("Escribe 'salir' para terminar.\n")

    if user_input.lower() in ("salir", "exit", "quit"):
        return

    if user_input.lower().startswith("guardar:"):
        payload = user_input[len("guardar:"):].strip()
        if "|" not in payload:
            print("Formato correcto: guardar: Titulo | Texto\n")
            return

        title, text = [x.strip() for x in payload.split("|", 1)]
        md = f"# {title}\n\n{text}\n"
        path = save_note(title, md)
        print(f" Guardado en: {path}\n")
        return

    groq.init(api_key=API_KEY)
    resp = groq.generate(
        model=MODEL,
        prompt=f"{SYSTEM}\n\nUser: {user_input}",
        max_tokens=1024,
    )
    print("\nAgente:", resp["output"].strip(), "\n")
    time.sleep(2)

if __name__ == "__main__":
    main()