"""
Agencia IA - Execution Model

Dataclass representing the agent_execution table.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class ExecutionModel:
    """Represents an agent execution record."""

    id: Optional[int] = None
    agent_id: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_ms: int = 0
    status: str = "running"
    input_summary: str = ""
    output_summary: str = ""
    error_message: str = ""
    model_used: str = ""
    tokens_used: int = 0
    trace_id: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "agent_id": self.agent_id,
            "duration_ms": self.duration_ms,
            "status": self.status,
            "model_used": self.model_used,
            "tokens_used": self.tokens_used,
            "error_message": self.error_message,
        }
