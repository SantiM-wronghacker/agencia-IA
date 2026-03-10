"""
Rutas y aplicación FastAPI para el Dashboard API v2.
"""
from __future__ import annotations

import logging
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Any, Optional

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .models import DashboardMetrics, HealthResponse, TaskCreate, TaskSchema, TaskStatus
from .repository import TaskRepository
from .websocket import ConnectionManager

logger = logging.getLogger(__name__)

# --- Aplicación FastAPI -----------------------------------------------------

app = FastAPI(
    title="Dashboard API v2",
    version="2.0.0",
    description="API para el dashboard de la agencia IA",
)

_allowed_origins = os.environ.get("DASHBOARD_CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register TeamDirector endpoint (feature-flag gated)
from ..agents_endpoint import register_team_director_routes

register_team_director_routes(app)

# --- Persistencia (SQLite) --------------------------------------------------

_start_time: float = time.time()
repo = TaskRepository()
manager = ConnectionManager()


# --- Helpers -----------------------------------------------------------------


def _event_envelope(event: str, payload: Any = None) -> dict[str, Any]:
    """Build a unified WebSocket event envelope.

    Contract: ``{ "event": str, "ts": str, "payload": ... }``
    """
    return {
        "event": event,
        "ts": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }


# --- PATCH body model -------------------------------------------------------


class TaskUpdate(BaseModel):
    """Campos opcionales para actualizar una tarea vía PATCH."""
    name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None


# --- Endpoints --------------------------------------------------------------


@app.get("/api/v2/dashboard/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Estado de salud del servicio."""
    return HealthResponse(
        status="ok",
        version=app.version,
        uptime=time.time() - _start_time,
        services={
            "api": "running",
            "websocket": f"{len(manager.active_connections)} conexiones",
        },
    )


@app.get("/api/v2/dashboard/metrics", response_model=DashboardMetrics)
async def metrics() -> DashboardMetrics:
    """Métricas en tiempo real calculadas vía query agregada SQLite."""
    data = repo.metrics()
    return DashboardMetrics(**data)


@app.post("/api/v2/dashboard/tasks", response_model=TaskSchema, status_code=status.HTTP_201_CREATED)
async def create_task(body: TaskCreate) -> TaskSchema:
    """Crea una nueva tarea."""
    now = datetime.now(timezone.utc)
    task = TaskSchema(
        id=str(uuid.uuid4()),
        name=body.name,
        description=body.description,
        status=TaskStatus.PENDING,
        created_at=now,
        updated_at=now,
    )
    repo.create(task)
    await manager.broadcast(
        _event_envelope("task_created", task.model_dump(mode="json"))
    )
    return task


@app.get("/api/v2/dashboard/tasks", response_model=list[TaskSchema])
async def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
) -> list[TaskSchema]:
    """Lista tareas con filtros opcionales de estado y búsqueda."""
    sf = status_filter.value if status_filter is not None else None
    return repo.list_all(status_filter=sf, search=search)


@app.get("/api/v2/dashboard/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str) -> TaskSchema:
    """Obtiene una tarea por su ID."""
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task


@app.patch("/api/v2/dashboard/tasks/{task_id}", response_model=TaskSchema)
async def update_task(task_id: str, body: TaskUpdate) -> TaskSchema:
    """Actualiza campos de una tarea existente (PATCH)."""
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        return task

    for field, value in update_data.items():
        setattr(task, field, value)
    task.updated_at = datetime.now(timezone.utc)
    repo.update(task)

    await manager.broadcast(
        _event_envelope("task_updated", task.model_dump(mode="json"))
    )
    return task


@app.post("/api/v2/dashboard/tasks/{task_id}/cancel", response_model=TaskSchema)
async def cancel_task(task_id: str) -> TaskSchema:
    """Cancela una tarea si está en estado PENDING o RUNNING."""
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    if task.status not in (TaskStatus.PENDING, TaskStatus.RUNNING):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cancelar una tarea con estado {task.status.value}",
        )

    task.status = TaskStatus.CANCELLED
    task.updated_at = datetime.now(timezone.utc)
    repo.update(task)
    await manager.broadcast(
        _event_envelope("task_cancelled", task.model_dump(mode="json"))
    )
    return task


@app.get("/api/v2/dashboard/tasks/{task_id}/logs", response_model=list[str])
async def get_task_logs(task_id: str) -> list[str]:
    """Devuelve los logs de una tarea."""
    task = repo.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task.logs


@app.websocket("/api/v2/dashboard/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    """Endpoint WebSocket para actualizaciones en tiempo real."""
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(
                _event_envelope("echo", data), websocket
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket)
