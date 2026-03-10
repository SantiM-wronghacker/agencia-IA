"""
RoleAgent – a specialised agent bound to a named role.

Each RoleAgent only has access to its own pre-registered tools/sub-agents.
It **cannot** execute arbitrary scripts or call tools outside its scope.
"""
from __future__ import annotations

import logging
from typing import Any, Callable

logger = logging.getLogger(__name__)


class RoleAgent:
    """An agent that is scoped to a single *role* (e.g. ``strategy``, ``tech``).

    Parameters
    ----------
    role:
        Short slug that identifies this role (e.g. ``"strategy"``).
    description:
        Human-readable description of the role's purpose.
    handler:
        Callable that performs the role's work.
        Signature: ``(goal: str, context: dict) -> dict``
    """

    def __init__(
        self,
        role: str,
        description: str,
        handler: Callable[..., dict[str, Any]],
    ) -> None:
        self.role = role
        self.description = description
        self._handler = handler

    def execute(self, goal: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Run the role handler with the given *goal* and optional *context*."""
        ctx = context or {}
        logger.info("RoleAgent[%s] executing goal: %s", self.role, goal)
        return self._handler(goal, ctx)

    def __repr__(self) -> str:
        return f"RoleAgent(role={self.role!r})"
