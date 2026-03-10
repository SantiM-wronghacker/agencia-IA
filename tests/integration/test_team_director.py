"""Tests for RoleAgent and TeamDirector – security + role isolation."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from src.agencia.agents.builder.role_agent import RoleAgent
from src.agencia.agents.builder.team_director import TeamDirector
from src.agencia.agents.builder.default_roles import BUILTIN_ROLES


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _echo_handler(goal, context):
    return {"echo": goal, "ctx": context}


def _make_director(*roles):
    td = TeamDirector(name="test-team")
    for r in roles:
        td.register(r)
    return td


# ---------------------------------------------------------------------------
# RoleAgent
# ---------------------------------------------------------------------------


class TestRoleAgent:
    def test_execute_returns_handler_result(self):
        agent = RoleAgent("tester", "Test role", _echo_handler)
        result = agent.execute("do stuff")
        assert result["echo"] == "do stuff"

    def test_context_forwarded(self):
        agent = RoleAgent("tester", "Test role", _echo_handler)
        result = agent.execute("x", context={"key": "val"})
        assert result["ctx"]["key"] == "val"


# ---------------------------------------------------------------------------
# TeamDirector
# ---------------------------------------------------------------------------


class TestTeamDirector:
    def test_register_and_list_roles(self):
        td = _make_director(
            RoleAgent("a", "A", _echo_handler),
            RoleAgent("b", "B", _echo_handler),
        )
        assert sorted(td.registered_roles) == ["a", "b"]

    def test_duplicate_registration_raises(self):
        td = _make_director(RoleAgent("a", "A", _echo_handler))
        with pytest.raises(ValueError, match="already registered"):
            td.register(RoleAgent("a", "A2", _echo_handler))

    def test_run_all_roles(self):
        td = _make_director(
            RoleAgent("x", "X", _echo_handler),
            RoleAgent("y", "Y", _echo_handler),
        )
        result = td.run("goal1")
        assert result["goal"] == "goal1"
        assert "x" in result["results"]
        assert "y" in result["results"]

    def test_run_subset_of_roles(self):
        td = _make_director(
            RoleAgent("x", "X", _echo_handler),
            RoleAgent("y", "Y", _echo_handler),
        )
        result = td.run("goal2", roles=["x"])
        assert "x" in result["results"]
        assert "y" not in result["results"]

    # -- Security: no arbitrary scripts ------------------------------------

    def test_rejects_unregistered_role(self):
        """TeamDirector must NOT allow execution of roles that are not
        registered – this prevents arbitrary script execution."""
        td = _make_director(RoleAgent("safe", "Safe", _echo_handler))
        with pytest.raises(ValueError, match="Unregistered roles"):
            td.run("evil goal", roles=["safe", "exec_shell"])

    def test_rejects_completely_unknown_role(self):
        td = TeamDirector()
        with pytest.raises(ValueError, match="Unregistered roles"):
            td.run("anything", roles=["arbitrary_script"])

    # -- Role isolation: sub-agents stay internal --------------------------

    def test_role_handler_receives_team_context(self):
        """A role's handler receives context about *which* team it belongs to,
        but cannot reach other roles' handlers directly."""
        called_with = {}

        def spy_handler(goal, context):
            called_with.update(context)
            return {"ok": True}

        td = _make_director(RoleAgent("spy", "Spy", spy_handler))
        td.run("check context")
        assert called_with.get("team") == "test-team"

    def test_builtin_roles_registered(self):
        """Built-in roles are available in BUILTIN_ROLES."""
        assert "strategy" in BUILTIN_ROLES
        assert "tech" in BUILTIN_ROLES


# ---------------------------------------------------------------------------
# CLI entrypoint (run.py)
# ---------------------------------------------------------------------------


class TestCLI:
    def test_main_success(self, capsys):
        from src.agencia.agents.builder.run import main

        main(["--goal", "Test goal", "--roles", "strategy"])
        out = capsys.readouterr().out
        assert "strategy" in out
        assert "Test goal" in out

    def test_main_invalid_role(self):
        from src.agencia.agents.builder.run import main

        with pytest.raises(SystemExit) as exc_info:
            main(["--goal", "Bad", "--roles", "nonexistent"])
        assert exc_info.value.code == 1
