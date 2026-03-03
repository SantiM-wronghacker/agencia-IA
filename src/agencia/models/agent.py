"""
Agencia IA - Agent Model

Dataclass representing the agent_registry table.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass
class AgentModel:
    """Represents an agent in the database."""

    id: Optional[int] = None
    name: str = ""
    category: str = ""
    subcategory: str = ""
    description: str = ""
    module_path: str = ""
    capabilities: list[str] = field(default_factory=list)
    version: str = "1.0.0"
    status: str = "active"
    preferred_model: str = "groq"
    config: dict[str, Any] = field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "subcategory": self.subcategory,
            "description": self.description,
            "module_path": self.module_path,
            "capabilities": self.capabilities,
            "version": self.version,
            "status": self.status,
            "preferred_model": self.preferred_model,
        }
