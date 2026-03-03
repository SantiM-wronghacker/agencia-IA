"""Tests for core utilities (no Ollama required)."""
from pathlib import Path


def test_load_state_missing_file(tmp_path):
    from agencia.agents.herramientas.core import load_state
    state = load_state(state_file=tmp_path / "nonexistent.json")
    assert state == {"summary": "", "recent": []}


def test_save_and_load_state(tmp_path):
    from agencia.agents.herramientas.core import save_state, load_state
    sf = tmp_path / "state.json"
    state = {"summary": "test summary", "recent": [{"role": "user", "content": "hi"}]}
    save_state(state, state_file=sf)
    loaded = load_state(state_file=sf)
    assert loaded == state


def test_add_recent_trims():
    from agencia.agents.herramientas.core import add_recent
    state = {"summary": "", "recent": []}
    for i in range(30):
        state = add_recent(state, "user", f"msg {i}", max_recent_turns=5)
    # max_recent_turns=5 means 5*2=10 messages max
    assert len(state["recent"]) == 10


def test_format_recent():
    from agencia.agents.herramientas.core import format_recent
    state = {"recent": [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi there"},
    ]}
    result = format_recent(state, n_msgs=2)
    assert "user: hello" in result
    assert "assistant: hi there" in result


def test_build_context_prefix_empty():
    from agencia.agents.herramientas.core import build_context_prefix
    assert build_context_prefix({"summary": ""}) == ""


def test_build_context_prefix_with_summary():
    from agencia.agents.herramientas.core import build_context_prefix
    result = build_context_prefix({"summary": "important context"})
    assert "MEMORIA" in result
    assert "important context" in result


def test_save_md(tmp_path):
    from agencia.agents.herramientas.core import save_md
    path = save_md("Test Title", "# Content here", runs_dir=tmp_path)
    assert Path(path).exists()
    content = Path(path).read_text(encoding="utf-8")
    assert "# Content here" in content
    assert "Test_Title" in path
