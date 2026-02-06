import json
from pathlib import Path
import streamlit as st
import subprocess
import os
import sys
import requests

BASE = Path(".")
PROJECTS_DIR = BASE / "projects"
PROJECTS_DIR.mkdir(exist_ok=True)

DEFAULT_AGENTS = [
    {"id": "chat", "name": "Chat", "enabled": True},
    {"id": "rag", "name": "RAG PRO", "enabled": True},
    {"id": "save", "name": "Save (notes)", "enabled": True},
    {"id": "task", "name": "Task (Planner+Executor)", "enabled": True},
    {"id": "router", "name": "Router", "enabled": True},
]

def ensure_project(company: str, project: str) -> Path:
    p = PROJECTS_DIR / company / project
    (p / "kb").mkdir(parents=True, exist_ok=True)
    (p / "runs").mkdir(parents=True, exist_ok=True)
    (p / "memory_db").mkdir(parents=True, exist_ok=True)
    cfg = p / "config.json"
    if not cfg.exists():
        cfg.write_text(json.dumps({"agents": DEFAULT_AGENTS}, ensure_ascii=False, indent=2), encoding="utf-8")
    state = p / "runs" / "state.json"
    if not state.exists():
        state.write_text(json.dumps({"summary": "", "recent": []}, ensure_ascii=False, indent=2), encoding="utf-8")
    return p

def list_companies():
    return sorted([d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()])

def list_projects(company: str):
    cdir = PROJECTS_DIR / company
    if not cdir.exists(): return []
    return sorted([d.name for d in cdir.iterdir() if d.is_dir()])

def load_config(p: Path):
    return json.loads((p / "config.json").read_text(encoding="utf-8"))

def save_config(p: Path, cfg: dict):
    (p / "config.json").write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")

def read_text_safe(path: Path, max_chars=20000):
    if not path.exists(): 
        return ""
    t = path.read_text(encoding="utf-8", errors="ignore")
    return t[:max_chars]

st.set_page_config(page_title="Agentes Locales - Panel", layout="wide")

st.title("Panel: Empresas → Proyectos → Agentes (Local)")

# Sidebar: Empresa / Proyecto
st.sidebar.header("Navegación")

companies = list_companies()
new_company = st.sidebar.text_input("Crear/Seleccionar empresa", value=(companies[0] if companies else "mi_empresa"))

projects = list_projects(new_company)
new_project = st.sidebar.text_input("Crear/Seleccionar proyecto", value=(projects[0] if projects else "default"))

p = ensure_project(new_company, new_project)

st.sidebar.markdown("---")
st.sidebar.write("Ruta del proyecto:")
st.sidebar.code(str(p.resolve()))

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Agentes", "KB / Index", "Memoria", "Runs", "Chat"])

# TAB 1: Agentes asignados
with tab1:
    st.subheader("Agentes asignados a este proyecto")
    cfg = load_config(p)
    agents = cfg.get("agents", [])

    colA, colB = st.columns([2, 1])

    with colA:
        for i, a in enumerate(agents):
            agents[i]["enabled"] = st.checkbox(f"{a['name']} ({a['id']})", value=a.get("enabled", True), key=f"agent_{a['id']}")
        if st.button("Guardar configuración de agentes"):
            cfg["agents"] = agents
            save_config(p, cfg)
            st.success("Configuración guardada en config.json")

    with colB:
        st.markdown("### Acciones")
        st.info("Este panel es UI. El chat/ejecución se conecta al router en el siguiente paso.")
        st.write("**Siguiente**: conectar botón 'Abrir chat' al script del router.")
        st.markdown("---")
        st.write("Config actual:")
        st.json(cfg)

# TAB 2: KB
with tab2:
    st.subheader("Base de Conocimiento (KB)")
    kb_dir = p / "kb"
    st.write("Pon archivos .txt/.md en:", str(kb_dir))
    kb_files = sorted([f.name for f in kb_dir.glob("*") if f.is_file()])
    st.write("Archivos en KB:", kb_files if kb_files else "Vacío")

    st.markdown("### Editor rápido")
    fname = st.text_input("Nombre de archivo (ej: precios.md)", value="notas.md")
    fpath = kb_dir / fname

    content = st.text_area("Contenido", value=read_text_safe(fpath), height=260)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Guardar archivo"):
            fpath.write_text(content, encoding="utf-8")
            st.success(f"Guardado: {fname}")
    with c2:
        st.warning("Indexar aquí requiere conectar tu indexador por proyecto (lo hacemos en el siguiente paso).")

# TAB 3: Memoria
with tab3:
    st.subheader("Memoria de conversación (state.json)")
    state_path = p / "runs" / "state.json"
    st.code(str(state_path))
    st.text_area("Contenido", value=read_text_safe(state_path, max_chars=50000), height=350)

    if st.button("Reset memoria (state.json)"):
        state_path.write_text(json.dumps({"summary": "", "recent": []}, ensure_ascii=False, indent=2), encoding="utf-8")
        st.success("Memoria reseteada.")

# TAB 4: Runs
with tab4:
    st.subheader("Entregables / Runs (.md)")
    runs_dir = p / "runs"
    md_files = sorted(runs_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True)
    st.write(f"Runs encontrados: {len(md_files)}")

    if md_files:
        chosen = st.selectbox("Abrir run", [f.name for f in md_files])
        st.text_area("Contenido del run", value=read_text_safe(runs_dir / chosen, max_chars=80000), height=380)
    else:
        st.info("Aún no hay runs en este proyecto.")

with tab5:
    st.subheader("Chat con agentes (por empresa/proyecto)")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Mostrar historial
    for msg in st.session_state.chat_history:
        st.chat_message(msg["role"]).markdown(msg["content"])

    user_input = st.chat_input("Escribe tu mensaje...")

    if user_input:
        st.chat_message("user").markdown(user_input)

        payload = {
            "company": new_company,
            "project": new_project,
            "message": user_input
        }

        try:
            res = requests.post("http://127.0.0.1:8000/chat", json=payload, timeout=120)
            data = res.json()
            answer = data.get("response", "Error: no response")
            route = data.get("route", "CHAT")
        except Exception as e:
            answer = f"❌ Error llamando al backend: {e}"
            route = "ERROR"

        st.chat_message("assistant").markdown(answer)
        st.caption(f"Ruta usada: {route}")

        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

    st.markdown("---")
    if st.button("Limpiar chat (solo UI)"):
        st.session_state.chat_history = []
        st.success("Chat limpiado.")

