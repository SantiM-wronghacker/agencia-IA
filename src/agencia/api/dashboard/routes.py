"""
Rutas y aplicación FastAPI para el Dashboard API v2.
"""
from __future__ import annotations

import logging
import os
import time
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, HTTPException, Query, WebSocket, WebSocketDisconnect, status
from fastapi.middleware.cors import CORSMiddleware

from .models import DashboardMetrics, HealthResponse, TaskCreate, TaskSchema, TaskStatus
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

# --- Estado en memoria ------------------------------------------------------

_start_time: float = time.time()
_task_store: dict[str, TaskSchema] = {}
manager = ConnectionManager()

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
    """Métricas en tiempo real calculadas a partir del store de tareas."""
    tasks = list(_task_store.values())
    total = len(tasks)
    completed = sum(1 for t in tasks if t.status == TaskStatus.COMPLETED)
    failed = sum(1 for t in tasks if t.status == TaskStatus.FAILED)
    pending = sum(1 for t in tasks if t.status == TaskStatus.PENDING)
    running = sum(1 for t in tasks if t.status == TaskStatus.RUNNING)
    success_rate = (completed / total * 100.0) if total > 0 else 0.0

    return DashboardMetrics(
        total_tasks=total,
        completed=completed,
        failed=failed,
        pending=pending,
        running=running,
        success_rate=round(success_rate, 2),
    )


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
    _task_store[task.id] = task
    await manager.broadcast({"event": "task_created", "task": task.model_dump(mode="json")})
    return task


@app.get("/api/v2/dashboard/tasks", response_model=list[TaskSchema])
async def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    search: Optional[str] = Query(None),
) -> list[TaskSchema]:
    """Lista tareas con filtros opcionales de estado y búsqueda."""
    tasks = list(_task_store.values())

    if status_filter is not None:
        tasks = [t for t in tasks if t.status == status_filter]

    if search:
        query = search.lower()
        tasks = [
            t for t in tasks
            if query in t.name.lower() or (t.description and query in t.description.lower())
        ]

    return tasks


@app.get("/api/v2/dashboard/tasks/{task_id}", response_model=TaskSchema)
async def get_task(task_id: str) -> TaskSchema:
    """Obtiene una tarea por su ID."""
    task = _task_store.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")
    return task


@app.post("/api/v2/dashboard/tasks/{task_id}/cancel", response_model=TaskSchema)
async def cancel_task(task_id: str) -> TaskSchema:
    """Cancela una tarea si está en estado PENDING o RUNNING."""
    task = _task_store.get(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada")

    if task.status not in (TaskStatus.PENDING, TaskStatus.RUNNING):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cancelar una tarea con estado {task.status.value}",
        )

    task.status = TaskStatus.CANCELLED
    task.updated_at = datetime.now(timezone.utc)
    _task_store[task_id] = task
    await manager.broadcast({"event": "task_cancelled", "task": task.model_dump(mode="json")})
    return task


@app.get("/api/v2/dashboard/tasks/{task_id}/logs", response_model=list[str])
async def get_task_logs(task_id: str) -> list[str]:
    """Devuelve los logs de una tarea."""
    task = _task_store.get(task_id)
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
            await manager.send_personal_message({"event": "echo", "data": data}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
