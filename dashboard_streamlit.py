"""
Dashboard Avanzado – Agencia IA
================================
Streamlit multi-página que consume la API v2 del Dashboard
(por defecto en http://localhost:8001).

Ejecutar:
    streamlit run dashboard_streamlit.py
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import streamlit as st

# ---------------------------------------------------------------------------
# Configuración persistente
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(__file__).resolve().parent / "config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "api_url": "http://localhost:8001",
    "theme": "light",
    "refresh_interval": 30,
}


def load_config() -> dict[str, Any]:
    """Carga la configuración desde *config.json* o devuelve los valores por defecto."""
    if CONFIG_PATH.exists():
        try:
            with open(CONFIG_PATH, encoding="utf-8") as fh:
                return {**DEFAULT_CONFIG, **json.load(fh)}
        except (json.JSONDecodeError, OSError) as exc:
            import logging as _logging

            _logging.getLogger(__name__).warning("Error al leer config.json: %s", exc)
    return dict(DEFAULT_CONFIG)


def save_config(cfg: dict[str, Any]) -> None:
    """Persiste la configuración en *config.json*."""
    with open(CONFIG_PATH, "w", encoding="utf-8") as fh:
        json.dump(cfg, fh, indent=2, ensure_ascii=False)


# Inicializar session_state
if "cfg" not in st.session_state:
    st.session_state.cfg = load_config()

# ---------------------------------------------------------------------------
# Helpers HTTP
# ---------------------------------------------------------------------------

API_BASE: str = st.session_state.cfg.get("api_url", DEFAULT_CONFIG["api_url"])


def _url(path: str) -> str:
    return f"{API_BASE}{path}"


def api_get(path: str, params: dict | None = None, timeout: int = 10) -> dict | list | None:
    """GET genérico con manejo de errores."""
    try:
        resp = requests.get(_url(path), params=params, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def api_post(path: str, json_body: dict | None = None, timeout: int = 10) -> dict | None:
    """POST genérico."""
    try:
        resp = requests.post(_url(path), json=json_body, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def api_patch(path: str, json_body: dict | None = None, timeout: int = 10) -> dict | None:
    """PATCH genérico."""
    try:
        resp = requests.patch(_url(path), json=json_body, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except requests.RequestException:
        return None


def api_delete_task(task_id: str) -> bool:
    """Cancela (elimina lógicamente) una tarea."""
    result = api_post(f"/api/v2/dashboard/tasks/{task_id}/cancel")
    return result is not None


# ---------------------------------------------------------------------------
# Cached data loaders
# ---------------------------------------------------------------------------


@st.cache_data(ttl=15)
def fetch_health() -> dict | None:
    return api_get("/api/v2/dashboard/health")


@st.cache_data(ttl=10)
def fetch_metrics() -> dict | None:
    return api_get("/api/v2/dashboard/metrics")


@st.cache_data(ttl=10)
def fetch_tasks(status_filter: str | None = None, search: str | None = None) -> list[dict]:
    params: dict[str, str] = {}
    if status_filter:
        params["status"] = status_filter
    if search:
        params["search"] = search
    result = api_get("/api/v2/dashboard/tasks", params=params)
    return result if isinstance(result, list) else []


# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Agencia IA – Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Sidebar – Navegación
# ---------------------------------------------------------------------------

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/artificial-intelligence.png", width=64)
    st.title("Agencia IA")
    page = st.radio(
        "Navegación",
        ["📊 Dashboard", "📋 Tareas", "📈 Análisis", "⚙️ Configuración"],
        label_visibility="collapsed",
    )
    st.divider()

    # Quick health indicator
    health = fetch_health()
    if health:
        st.success("🟢 API Online")
    else:
        st.error("🔴 API Offline")

    st.caption(f"API: {API_BASE}")

# ============================================================================
# PAGE: Dashboard
# ============================================================================

if page == "📊 Dashboard":
    st.header("📊 Dashboard Principal")

    # --- KPIs ---------------------------------------------------------------
    metrics = fetch_metrics()
    if metrics is None:
        st.warning("⚠️ No se pudo conectar con la API. Verifica que esté corriendo.")
        st.stop()

    kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
    kpi1.metric("Total Tareas", metrics.get("total_tasks", 0))
    kpi2.metric("✅ Completadas", metrics.get("completed", 0))
    kpi3.metric("❌ Fallidas", metrics.get("failed", 0))
    kpi4.metric("⏳ Pendientes", metrics.get("pending", 0))
    kpi5.metric("🔄 En Progreso", metrics.get("running", 0))

    st.divider()

    col_rate, col_health = st.columns(2)

    with col_rate:
        st.subheader("Tasa de Éxito")
        rate = metrics.get("success_rate", 0)
        fig_gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=rate,
                number={"suffix": "%"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "#2ecc71"},
                    "steps": [
                        {"range": [0, 50], "color": "#fdecea"},
                        {"range": [50, 80], "color": "#fef9e7"},
                        {"range": [80, 100], "color": "#eafaf1"},
                    ],
                },
            )
        )
        fig_gauge.update_layout(height=250, margin=dict(t=30, b=10, l=30, r=30))
        st.plotly_chart(fig_gauge, use_container_width=True)

    with col_health:
        st.subheader("Estado de Servicios")
        if health:
            for svc, status_val in health.get("services", {}).items():
                st.markdown(f"- **{svc}**: `{status_val}`")
            st.info(f"Uptime: {health.get('uptime', 0):.0f} s  |  Versión: {health.get('version', '?')}")
        else:
            st.error("No se pudo obtener el estado de salud.")

    # --- Tendencias (simple: distribución actual) ---------------------------
    st.subheader("📈 Distribución de Tareas")
    tasks = fetch_tasks()
    if tasks:
        df = pd.DataFrame(tasks)
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["Estado", "Cantidad"]
        color_map = {
            "pending": "#f39c12",
            "running": "#3498db",
            "completed": "#2ecc71",
            "failed": "#e74c3c",
            "cancelled": "#95a5a6",
        }
        fig_bar = px.bar(
            status_counts,
            x="Estado",
            y="Cantidad",
            color="Estado",
            color_discrete_map=color_map,
            text_auto=True,
        )
        fig_bar.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("No hay tareas todavía.")

    # Nota: para auto-refresh, usar el botón de Streamlit o st.rerun() manualmente.

# ============================================================================
# PAGE: Tareas
# ============================================================================

elif page == "📋 Tareas":
    st.header("📋 Gestor de Tareas")

    # --- Filtros -------------------------------------------------------------
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        status_options = ["Todos", "pending", "running", "completed", "failed", "cancelled"]
        sel_status = st.selectbox("Filtrar por estado", status_options)
    with filter_col2:
        search_query = st.text_input("🔍 Buscar por nombre o descripción")

    status_param = sel_status if sel_status != "Todos" else None
    search_param = search_query if search_query else None

    # --- Crear tarea ---------------------------------------------------------
    st.subheader("➕ Crear Nueva Tarea")
    with st.form("create_task_form", clear_on_submit=True):
        new_name = st.text_input("Nombre de la tarea *")
        new_desc = st.text_area("Descripción (opcional)")
        submitted = st.form_submit_button("Crear Tarea", type="primary")
        if submitted:
            if not new_name.strip():
                st.error("El nombre es obligatorio.")
            else:
                with st.spinner("Creando tarea…"):
                    result = api_post(
                        "/api/v2/dashboard/tasks",
                        {"name": new_name.strip(), "description": new_desc.strip() or None},
                    )
                if result:
                    st.success(f"✅ Tarea **{result['name']}** creada (ID: `{result['id'][:8]}…`)")
                    st.cache_data.clear()
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Error al crear la tarea. Verifica la API.")

    st.divider()

    # --- Listar tareas -------------------------------------------------------
    st.subheader("📄 Tareas Existentes")
    # Clear cache to get fresh data after mutations
    tasks = fetch_tasks(status_param, search_param)

    if not tasks:
        st.info("No se encontraron tareas con los filtros seleccionados.")
    else:
        for task in tasks:
            tid = task["id"]
            status_icon = {
                "pending": "⏳",
                "running": "🔄",
                "completed": "✅",
                "failed": "❌",
                "cancelled": "🚫",
            }.get(task["status"], "❓")

            with st.expander(f"{status_icon} {task['name']}  —  `{tid[:8]}…`"):
                st.markdown(f"**Estado:** {task['status']}  \n**Descripción:** {task.get('description') or '—'}")
                st.markdown(f"**Creada:** {task.get('created_at', '?')}  \n**Actualizada:** {task.get('updated_at', '?')}")

                # --- Editar tarea ------------------------------------------------
                st.markdown("---")
                st.markdown("**✏️ Editar tarea**")
                edit_col1, edit_col2 = st.columns(2)
                with edit_col1:
                    edit_name = st.text_input("Nombre", value=task["name"], key=f"edit_name_{tid}")
                with edit_col2:
                    status_list = ["pending", "running", "completed", "failed", "cancelled"]
                    current_idx = status_list.index(task["status"]) if task["status"] in status_list else 0
                    edit_status = st.selectbox("Estado", status_list, index=current_idx, key=f"edit_status_{tid}")
                edit_desc = st.text_area(
                    "Descripción", value=task.get("description") or "", key=f"edit_desc_{tid}"
                )

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button("💾 Guardar cambios", key=f"save_{tid}"):
                        patch_body: dict[str, Any] = {}
                        if edit_name != task["name"]:
                            patch_body["name"] = edit_name
                        if edit_desc != (task.get("description") or ""):
                            patch_body["description"] = edit_desc if edit_desc else None
                        if edit_status != task["status"]:
                            patch_body["status"] = edit_status

                        if patch_body:
                            with st.spinner("Guardando…"):
                                res = api_patch(f"/api/v2/dashboard/tasks/{tid}", patch_body)
                            if res:
                                st.success("✅ Tarea actualizada.")
                                st.cache_data.clear()
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("❌ Error al actualizar.")
                        else:
                            st.info("No hay cambios que guardar.")

                with btn_col2:
                    if task["status"] in ("pending", "running"):
                        if st.button("🚫 Cancelar tarea", key=f"cancel_{tid}"):
                            with st.spinner("Cancelando…"):
                                ok = api_delete_task(tid)
                            if ok:
                                st.warning("Tarea cancelada.")
                                st.cache_data.clear()
                                time.sleep(0.5)
                                st.rerun()
                            else:
                                st.error("Error al cancelar.")

# ============================================================================
# PAGE: Análisis
# ============================================================================

elif page == "📈 Análisis":
    st.header("📈 Análisis de Tareas")

    tasks = fetch_tasks()
    if not tasks:
        st.info("No hay tareas para analizar.")
        st.stop()

    df = pd.DataFrame(tasks)

    # --- Distribución de estados (Pie chart) --------------------------------
    col_pie, col_line = st.columns(2)

    with col_pie:
        st.subheader("Distribución por Estado")
        status_counts = df["status"].value_counts().reset_index()
        status_counts.columns = ["Estado", "Cantidad"]
        color_map = {
            "pending": "#f39c12",
            "running": "#3498db",
            "completed": "#2ecc71",
            "failed": "#e74c3c",
            "cancelled": "#95a5a6",
        }
        fig_pie = px.pie(
            status_counts,
            values="Cantidad",
            names="Estado",
            color="Estado",
            color_discrete_map=color_map,
            hole=0.4,
        )
        fig_pie.update_layout(height=350)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- Tareas por fecha (Line chart) --------------------------------------
    with col_line:
        st.subheader("Tareas por Fecha de Creación")
        if "created_at" in df.columns:
            df["date"] = pd.to_datetime(df["created_at"], errors="coerce").dt.date
            daily = df.groupby("date").size().reset_index(name="Cantidad")
            daily.columns = ["Fecha", "Cantidad"]
            fig_line = px.line(
                daily,
                x="Fecha",
                y="Cantidad",
                markers=True,
                line_shape="spline",
            )
            fig_line.update_layout(height=350)
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No hay datos de fecha disponibles.")

    st.divider()

    # --- Estadísticas resumen -----------------------------------------------
    st.subheader("📊 Estadísticas Generales")
    metrics = fetch_metrics()
    if metrics:
        stat_cols = st.columns(3)
        stat_cols[0].metric("Total", metrics["total_tasks"])
        stat_cols[1].metric("Tasa de éxito", f"{metrics['success_rate']}%")
        stat_cols[2].metric("Fallidas", metrics["failed"])

    # --- Top tareas recientes -----------------------------------------------
    st.subheader("🕐 Tareas Más Recientes")
    if "created_at" in df.columns:
        df_sorted = df.sort_values("created_at", ascending=False)
    else:
        df_sorted = df
    top_n = min(10, len(df_sorted))
    display_cols = [c for c in ["name", "status", "created_at", "description"] if c in df_sorted.columns]
    st.dataframe(df_sorted.head(top_n)[display_cols], use_container_width=True, hide_index=True)

# ============================================================================
# PAGE: Configuración
# ============================================================================

elif page == "⚙️ Configuración":
    st.header("⚙️ Configuración del Dashboard")

    cfg = st.session_state.cfg

    with st.form("config_form"):
        api_url = st.text_input("URL de la API", value=cfg.get("api_url", DEFAULT_CONFIG["api_url"]))
        theme = st.selectbox(
            "Tema",
            ["light", "dark"],
            index=0 if cfg.get("theme", "light") == "light" else 1,
        )
        refresh = st.number_input(
            "Intervalo de refresh (segundos)",
            min_value=5,
            max_value=300,
            value=cfg.get("refresh_interval", 30),
            step=5,
        )
        save_btn = st.form_submit_button("💾 Guardar Preferencias", type="primary")

        if save_btn:
            new_cfg = {"api_url": api_url.strip(), "theme": theme, "refresh_interval": int(refresh)}
            save_config(new_cfg)
            st.session_state.cfg = new_cfg
            st.success("✅ Configuración guardada correctamente.")
            time.sleep(0.5)
            st.rerun()

    st.divider()
    st.subheader("📄 Configuración Actual")
    st.json(cfg)

    if CONFIG_PATH.exists():
        st.caption(f"Archivo: `{CONFIG_PATH}`")
    else:
        st.caption("Aún no se ha guardado un archivo de configuración.")
