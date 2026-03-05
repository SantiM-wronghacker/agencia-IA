"""
TeamDirector – role-gated task orchestrator.

Provides a simple director that only accepts registered roles and
exposes both a FastAPI dev-endpoint and a thin CLI wrapper.
"""
from __future__ import annotations

import argparse
import sys
from typing import Any

from .models import UserRole

# Registered roles that the director accepts.
REGISTERED_ROLES: frozenset[str] = frozenset(r.value for r in UserRole)


class TeamDirector:
    """Orchestrates tasks ensuring only registered roles are used."""

    def __init__(self) -> None:
        self.history: list[dict[str, Any]] = []

    def assign(self, role: str, task_description: str) -> dict[str, Any]:
        """Assign a task to a role.

        Raises ``ValueError`` if the role is not registered.
        """
        if role not in REGISTERED_ROLES:
            raise ValueError(
                f"Role '{role}' is not registered. "
                f"Allowed roles: {sorted(REGISTERED_ROLES)}"
            )
        entry = {"role": role, "task": task_description, "status": "assigned"}
        self.history.append(entry)
        return entry


def cli(argv: list[str] | None = None) -> None:
    """Minimal CLI entrypoint for TeamDirector.

    Usage::

        python -m agencia.api.dashboard.team_director --role admin --task "Deploy v2"
    """
    parser = argparse.ArgumentParser(description="TeamDirector CLI")
    parser.add_argument("--role", required=True, help="Role to assign the task to")
    parser.add_argument("--task", required=True, help="Task description")
    args = parser.parse_args(argv)

    director = TeamDirector()
    try:
        result = director.assign(args.role, args.task)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    print(f"Assigned: role={result['role']}, task={result['task']}, status={result['status']}")


if __name__ == "__main__":
    cli()
