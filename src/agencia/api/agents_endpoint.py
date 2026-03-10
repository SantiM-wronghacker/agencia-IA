"""
FastAPI endpoint for TeamDirector (dev-only).

Activate with env ``USE_TEAM_DIRECTOR=true``.

    POST /api/v2/agents/run
    {
      "goal": "Launch MVP",
      "roles": ["strategy", "tech"]   // optional – omit for all roles
    }
"""
from __future__ import annotations

import logging
import os
from typing import Any, Optional

from pydantic import BaseModel

logger = logging.getLogger(__name__)

_USE_TEAM_DIRECTOR = os.getenv("USE_TEAM_DIRECTOR", "false").lower() == "true"


class AgentRunRequest(BaseModel):
    goal: str
    roles: Optional[list[str]] = None


class AgentRunResponse(BaseModel):
    goal: str
    results: dict[str, Any]


def register_team_director_routes(app: Any) -> None:
    """Register ``/api/v2/agents/run`` on *app* if the feature flag is set."""
    if not _USE_TEAM_DIRECTOR:
        logger.info("USE_TEAM_DIRECTOR is not set – TeamDirector endpoint disabled")
        return

    from ..agents.builder.default_roles import BUILTIN_ROLES
    from ..agents.builder.team_director import TeamDirector

    director = TeamDirector(name="api-team")
    for agent in BUILTIN_ROLES.values():
        director.register(agent)

    @app.post("/api/v2/agents/run", response_model=AgentRunResponse)
    async def run_agents(body: AgentRunRequest) -> AgentRunResponse:
        """Execute TeamDirector with the given goal and optional roles."""
        result = director.run(goal=body.goal, roles=body.roles)
        return AgentRunResponse(**result)

    logger.info("TeamDirector endpoint registered at /api/v2/agents/run")
