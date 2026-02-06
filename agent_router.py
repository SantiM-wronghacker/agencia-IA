import ollama
from datetime import datetime
from pathlib import Path

# === Config ===
MODEL = "llama3:8b"   # luego puedes cambiar a gpt-oss:20b para "decisiones"
RUNS_DIR = Path("runs")
KB_DIR = Path("kb")
RUNS_DIR.mkdir(exist_ok=True)
KB_DIR.mkdir(exist_ok=True)

SYSTEM_ROUTER = """Eres un Router (director) de un sistema de agentes.
Tu trabajo es clasificar la intención del usuario en UNA de estas rutas:

- CHAT: pregunta simple o conversación
- SAVE: el usuario quiere guardar una nota/idea en archivo
- TASK: quiere un plan + entregable (tarea compleja)
- RAG: pregunta que debe responderse usando conocimiento de la carpeta kb/

Devuelve SOLO una palabra: CHAT, SAVE, TASK o RAG.
Reglas:
- Si menciona "guardar", "anotar", "nota", "guardar:" => SAVE
- Si pide plan, estrategia, checklist, pasos, propuesta, documento => TASK
- Si pregunta precios, políticas, procesos internos, cosas que estarían en kb/ => RAG
- Si no estás seguro => CHAT
"""

SYSTEM_CHAT = "Eres un asistente útil, directo y práctico."
SYSTEM_PLANNER = """Eres un Planner. Convierte la petición en un plan accionable.
Devuelve:
1) Objetivo (1 línea)
2) Plan (5-10 pasos numerados)
3) Entregables
4) Riesgos y supuestos (breve)
"""
SYSTEM_EXEC = """Eres un Executor. Toma la petición y el plan y genera un primer entregable real.
Entrega en Markdown con checklist. Marca supuestos si faltan datos.
"""

def llm(system: str, user: str, model: str = MODEL) -> str:
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

def rag_search(query: str, top_k: int = 2) -> str:
    # RAG simple (sin embeddings): busca texto por coincidencias básicas.
    # Luego lo hacemos pro con Chroma/embeddings.
    files = list(KB_DIR.glob("*"))
    if not files:
        return "KB vacía: no hay archivos en kb/. Agrega docs (precios, procesos, etc.)."

    scored = []
    q = query.lower()
    for f in files:
        try:
            txt = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        score = sum(1 for w in q.split() if w in txt.lower())
        scored.append((score, f.name, txt))

    scored.sort(reverse=True, key=lambda x: x[0])
    top = scored[:top_k]
    context = []
    for score, name, txt in top:
        snippet = txt[:1500]  # recorte simple
        context.append(f"[Fuente: {name} | score={score}]\n{snippet}")
    return "\n\n---\n\n".join(context)

def handle_save(user: str) -> str:
    # Formato recomendado: guardar: Titulo | Texto
    if user.lower().startswith("guardar:") and "|" in user:
        payload = user[len("guardar:"):].strip()
        title, text = [x.strip() for x in payload.split("|", 1)]
    else:
        # Si no sigue formato, le pedimos a la IA que lo convierta en nota
        title = "nota"
        text = user

    md = f"# {title}\n\n{text}\n"
    path = save_md(title, md)
    return f"✅ Guardado en: {path}"

def handle_task(user: str) -> str:
    plan = llm(SYSTEM_PLANNER, user)
    deliverable = llm(SYSTEM_EXEC, f"Petición:\n{user}\n\nPlan:\n{plan}")
    report = f"# Tarea\n{user}\n\n# Plan (Planner)\n{plan}\n\n# Entregable (Executor)\n{deliverable}\n"
    path = save_md("tarea_router", report)
    return f"✅ Tarea resuelta y guardada en: {path}"

def handle_rag(user: str) -> str:
    context = rag_search(user, top_k=2)
    answer = llm(
        SYSTEM_CHAT,
        f"Responde usando SOLO la información de contexto. Si no está en el contexto, dilo.\n\nCONTEXTO:\n{context}\n\nPREGUNTA:\n{user}"
    )
    return answer

def main():
    print("Router listo. Escribe 'salir' para terminar.\n")
    print("Tips:")
    print("- Para guardar:  guardar: Titulo | Texto")
    print("- Archivos de memoria van en: kb/\n")

    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        route = llm(SYSTEM_ROUTER, user).upper().split()[0]
        if route not in ("CHAT", "SAVE", "TASK", "RAG"):
            route = "CHAT"

        if route == "SAVE":
            print("\nRouter → SAVE")
            print(handle_save(user), "\n")
        elif route == "TASK":
            print("\nRouter → TASK")
            print(handle_task(user), "\n")
        elif route == "RAG":
            print("\nRouter → RAG")
            print("\nAgente:", handle_rag(user), "\n")
        else:
            print("\nRouter → CHAT")
            print("\nAgente:", llm(SYSTEM_CHAT, user), "\n")

if __name__ == "__main__":
    main()
