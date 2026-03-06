"""Integration tests: verify all agent Python files compile without errors."""

import os
import py_compile
import pytest
from pathlib import Path

AGENTS_DIR = Path(__file__).resolve().parent.parent.parent / "src" / "agencia" / "agents"


def _collect_py_files():
    """Collect all .py files under src/agencia/agents/."""
    return sorted(str(p) for p in AGENTS_DIR.rglob("*.py") if p.name != "__pycache__")


@pytest.fixture(scope="module")
def agent_files():
    return _collect_py_files()


def test_agents_dir_exists():
    assert AGENTS_DIR.is_dir(), f"Agents directory not found: {AGENTS_DIR}"


def test_at_least_100_agents(agent_files):
    """The system should have at least 100 agent files."""
    assert len(agent_files) >= 100, f"Only {len(agent_files)} agents found, expected >= 100"


@pytest.mark.parametrize("py_file", _collect_py_files(), ids=lambda p: os.path.basename(p))
def test_agent_compiles(py_file):
    """Each agent Python file must compile without SyntaxError."""
    py_compile.compile(py_file, doraise=True)
