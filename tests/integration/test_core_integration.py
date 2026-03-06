"""Integration tests for core utilities and agent subsystems."""

import json
import os
import ast
import pytest
from pathlib import Path
from unittest.mock import patch


# ---- State management round-trip ----

def test_state_round_trip_with_unicode(tmp_path):
    """State files with Spanish characters should survive save/load."""
    from agencia.agents.herramientas.core import save_state, load_state
    sf = tmp_path / "state.json"
    state = {
        "summary": "Análisis de inversión en bienes raíces",
        "recent": [
            {"role": "user", "content": "¿Cuánto cuesta la propiedad?"},
            {"role": "assistant", "content": "El precio es $2,500,000 MXN"},
        ],
    }
    save_state(state, state_file=sf)
    loaded = load_state(state_file=sf)
    assert loaded["summary"] == state["summary"]
    assert loaded["recent"][0]["content"] == "¿Cuánto cuesta la propiedad?"


def test_save_md_creates_file(tmp_path):
    """save_md should create a timestamped markdown file."""
    from agencia.agents.herramientas.core import save_md
    path = save_md("Reporte Ventas", "# Resumen\nTotal: $500,000", runs_dir=tmp_path)
    p = Path(path)
    assert p.exists()
    assert p.suffix == ".md"
    content = p.read_text(encoding="utf-8")
    assert "# Resumen" in content


# ---- Supervisor QA ----

def test_supervisor_qa_verifies_syntax(tmp_path):
    """supervisor_qa should correctly identify valid Python syntax."""
    from agencia.agents.cerebro.supervisor_qa import verificar_sintaxis
    good_file = tmp_path / "good.py"
    good_file.write_text("x = 1 + 2\nprint(x)\n", encoding="utf-8")
    ok, error = verificar_sintaxis(str(good_file))
    assert ok is True
    assert error is None


def test_supervisor_qa_detects_bad_syntax(tmp_path):
    """supervisor_qa should detect broken Python syntax."""
    from agencia.agents.cerebro.supervisor_qa import verificar_sintaxis
    bad_file = tmp_path / "bad.py"
    bad_file.write_text("def f(\n", encoding="utf-8")
    ok, error = verificar_sintaxis(str(bad_file))
    assert ok is False
    assert error is not None


# ---- Estrategia ----

def test_estrategia_no_prohibited_imports():
    """agente_estrategia should have empty IMPORTS_PROHIBIDOS (all migrated)."""
    from agencia.agents.cerebro.agente_estrategia import IMPORTS_PROHIBIDOS
    assert len(IMPORTS_PROHIBIDOS) == 0


def test_estrategia_detects_no_false_positives(tmp_path):
    """Detection should not trigger on strings containing 'ollama' as text."""
    from agencia.agents.cerebro.agente_estrategia import tiene_imports_prohibidos
    # File that mentions 'ollama' in a string but doesn't import it
    test_file = tmp_path / "safe.py"
    test_file.write_text(
        'FORBIDDEN = ["ollama", "openai"]\nprint("checking ollama")\n',
        encoding="utf-8",
    )
    has_prohibited, found = tiene_imports_prohibidos(str(test_file))
    assert has_prohibited is False


# ---- Mapeador Capacidades ----

def test_mapeador_categorizes_correctly():
    """The categorizer should assign expected areas based on file names."""
    from agencia.agents.operaciones.mapeador_capacidades import categorizar
    assert categorizar("agent_router.py", "") == "CEREBRO"
    assert categorizar("calculadora_isr.py", "") == "FINANZAS"
    assert categorizar("simulador_hipoteca.py", "") == "REAL ESTATE"
    assert categorizar("formateador_moneda.py", "") == "HERRAMIENTAS"


def test_mapeador_no_contaminants():
    """CONTAMINANTES should be empty after Groq migration."""
    from agencia.agents.operaciones.mapeador_capacidades import CONTAMINANTES
    assert len(CONTAMINANTES) == 0


# ---- Reparador Masivo ----

def test_reparador_diagnosticar_clean_file(tmp_path):
    """diagnosticar should return empty list for a clean file."""
    from agencia.agents.herramientas.reparador_masivo import diagnosticar
    clean = tmp_path / "clean.py"
    clean.write_text('"""\nÁREA: TEST\n"""\nimport sys\ndef main():\n    x = sys.argv[1] if len(sys.argv) > 1 else "default"\n    print(x)\n', encoding="utf-8")
    os.chdir(tmp_path)
    problems = diagnosticar("clean.py")
    assert problems == []


def test_reparador_detects_input_usage(tmp_path):
    """diagnosticar should detect input() usage."""
    from agencia.agents.herramientas.reparador_masivo import diagnosticar
    bad = tmp_path / "with_input.py"
    bad.write_text('"""\nÁREA: TEST\n"""\ndef main():\n    x = input("Enter: ")\n    print(x)\n', encoding="utf-8")
    os.chdir(tmp_path)
    problems = diagnosticar("with_input.py")
    assert "USA_INPUT" in problems
