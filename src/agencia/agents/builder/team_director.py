"""
TeamDirector – orchestrates a set of registered RoleAgents.

Only roles that have been **explicitly registered** can be executed.
This prevents execution of arbitrary scripts or unregistered code.
"""
from __future__ import annotations

import logging
from typing import Any

from .role_agent import RoleAgent

logger = logging.getLogger(__name__)


class TeamDirector:
    """Coordinates a team of :class:`RoleAgent` instances.

    Parameters
    ----------
    name:
        Human-readable name for this team.
    """

    def __init__(self, name: str = "default-team") -> None:
        self.name = name
        self._roles: dict[str, RoleAgent] = {}

    # ---- registration ------------------------------------------------------

    def register(self, agent: RoleAgent) -> None:
        """Register a role agent.  Raises ``ValueError`` on duplicate."""
        if agent.role in self._roles:
            raise ValueError(f"Role '{agent.role}' is already registered")
        self._roles[agent.role] = agent
        logger.info("TeamDirector[%s]: registered role '%s'", self.name, agent.role)

    @property
    def registered_roles(self) -> list[str]:
        return list(self._roles.keys())

    # ---- execution ---------------------------------------------------------

    def run(
        self,
        goal: str,
        roles: list[str] | None = None,
    ) -> dict[str, Any]:
        """Execute the *goal* using the specified (or all) registered roles.

        Parameters
        ----------
        goal:
            The objective to accomplish.
        roles:
            Subset of role slugs to use.  If ``None``, all registered roles
            participate.

        Returns
        -------
        dict
            ``{ "goal": str, "results": { role_slug: result_dict, ... } }``

        Raises
        ------
        ValueError
            If any requested role is not registered (prevents arbitrary
            execution).
        """
        target_roles = roles if roles is not None else list(self._roles.keys())

        # Security gate: reject unknown roles
        unknown = set(target_roles) - set(self._roles.keys())
        if unknown:
            raise ValueError(
                f"Unregistered roles requested: {unknown}. "
                f"Available: {self.registered_roles}"
            )

        results: dict[str, Any] = {}
        for role_slug in target_roles:
            agent = self._roles[role_slug]
            logger.info("TeamDirector[%s]: dispatching to role '%s'", self.name, role_slug)
            results[role_slug] = agent.execute(goal, context={"team": self.name})

        return {"goal": goal, "results": results}

    def __repr__(self) -> str:
        return f"TeamDirector(name={self.name!r}, roles={self.registered_roles})"
