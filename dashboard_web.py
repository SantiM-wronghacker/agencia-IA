#!/usr/bin/env python3
"""
Dashboard Web - Punto de entrada.
Ejecuta dashboard_web.py con BASE_DIR apuntando al root del proyecto.
"""
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(root_dir, "src", "agencia", "agents", "herramientas", "dashboard_web.py")

if __name__ == "__main__":
    if not os.path.exists(script_path):
        print(f"ERROR: No se encontró {script_path}", file=sys.stderr)
        sys.exit(1)

    sys.path.insert(0, root_dir)
    sys.path.insert(0, os.path.dirname(script_path))
    os.chdir(root_dir)

    with open(script_path, "r", encoding="utf-8") as f:
        code = compile(f.read(), os.path.join(root_dir, "dashboard_web.py"), "exec")
    exec(code, {"__name__": "__main__", "__file__": os.path.join(root_dir, "dashboard_web.py")})
