#!/usr/bin/env python3
"""
Sistema Maestro v2.0 - Punto de entrada del proyecto.
Wrapper que redirige a la ejecución del Sistema Maestro desde src/agencia/agents/cerebro/
"""
import sys
import os
import subprocess

root_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(root_dir, "src", "agencia", "agents", "cerebro", "sistema_maestro.py")

if __name__ == "__main__":
    if not os.path.exists(script_path):
        print(f"ERROR: No se encontró {script_path}", file=sys.stderr)
        sys.exit(1)

    try:
        # Ejecutar el script real desde su directorio
        result = subprocess.run(
            [sys.executable, script_path],
            cwd=os.path.dirname(script_path),
            env={**os.environ, "PYTHONPATH": root_dir}
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"ERROR iniciando Sistema Maestro: {e}", file=sys.stderr)
        sys.exit(1)
