#!/usr/bin/env python3
"""
Sistema Maestro v2.0 - Punto de entrada.
Ejecuta el sistema maestro con BASE_DIR apuntando al root del proyecto.
"""
import sys
import os

root_dir = os.path.dirname(os.path.abspath(__file__))
script_path = os.path.join(root_dir, "src", "agencia", "agents", "cerebro", "sistema_maestro.py")

if __name__ == "__main__":
    if not os.path.exists(script_path):
        print(f"ERROR: No se encontró {script_path}", file=sys.stderr)
        sys.exit(1)

    # Añadir root y cerebro al path para imports
    sys.path.insert(0, root_dir)
    sys.path.insert(0, os.path.dirname(script_path))
    os.chdir(root_dir)

    # Ejecutar con __file__ apuntando al ROOT para que BASE_DIR = root
    with open(script_path, "r", encoding="utf-8") as f:
        code = compile(f.read(), os.path.join(root_dir, "sistema_maestro.py"), "exec")
    exec(code, {"__name__": "__main__", "__file__": os.path.join(root_dir, "sistema_maestro.py")})
