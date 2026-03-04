"""
Modelos Pydantic para el Dashboard API v2.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Estados posibles de una tarea."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class UserRole(str, Enum):
    """Roles de usuario."""
    ADMIN = "admin"
    USER = "user"
    VIEWER = "viewer"


class TaskCreate(BaseModel):
    """Esquema para crear una tarea."""
    name: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    """Esquema para actualizar una tarea (PATCH)."""
    name: Optional[str] = None
    status: Optional[TaskStatus] = None
    description: Optional[str] = None
    result: Optional[Any] = None


class RunAgentRequest(BaseModel):
    """Esquema para ejecutar un agente."""
    category: str
    agent_name: str
    input: str


class AlertConfig(BaseModel):
    """Configuración de alertas del dashboard."""
    max_failed: int = 5
    min_success_rate: float = 80.0


class TaskSchema(BaseModel):
    """Esquema completo de una tarea."""
    id: str
    name: str
    status: TaskStatus = TaskStatus.PENDING
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    result: Optional[Any] = None
    logs: list[str] = Field(default_factory=list)


class DashboardMetrics(BaseModel):
    """Métricas agregadas del dashboard."""
    total_tasks: int = 0
    completed: int = 0
    failed: int = 0
    pending: int = 0
    running: int = 0
    success_rate: float = 0.0
    avg_completion_time: Optional[float] = None


class HealthResponse(BaseModel):
    """Respuesta del endpoint de salud."""
    status: str
    version: str
    uptime: float
    services: dict[str, Any] = Field(default_factory=dict)


class TokenData(BaseModel):
    """Datos contenidos en un token JWT."""
    sub: str
    role: UserRole
    exp: datetime
