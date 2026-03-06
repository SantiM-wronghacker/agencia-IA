"""Integration tests: verify key agent scripts run standalone without crashing."""

import subprocess
import sys
import pytest

PYTHON = sys.executable


def _run_agent(module_path, args=None, timeout=15):
    """Run an agent script as subprocess and return (returncode, stdout, stderr)."""
    cmd = [PYTHON, "-m", module_path] + (args or [])
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=timeout,
        cwd=str(__import__("pathlib").Path(__file__).resolve().parent.parent.parent),
        env={**__import__("os").environ, "PYTHONPATH": "src"},
    )
    return result.returncode, result.stdout, result.stderr


def test_seguimiento_pipeline_runs():
    """seguimiento_pipeline should run with defaults and produce output."""
    code, stdout, stderr = _run_agent(
        "agencia.agents.ventas.seguimiento_pipeline"
    )
    assert code == 0, f"Exit code {code}, stderr: {stderr}"
    assert "VENTAS" in stdout
    assert "MXN" in stdout


def test_optimizador_ruta_runs():
    """optimizador_ruta_entregas should run with defaults."""
    code, stdout, stderr = _run_agent(
        "agencia.agents.logistica.optimizador_ruta_entregas"
    )
    assert code == 0, f"Exit code {code}, stderr: {stderr}"
    assert "km" in stdout


def test_config_runs():
    """config.py should print system configuration."""
    code, stdout, stderr = _run_agent(
        "agencia.agents.herramientas.config"
    )
    assert code == 0, f"Exit code {code}, stderr: {stderr}"
    assert "Groq" in stdout or "API" in stdout or "Directorio" in stdout
