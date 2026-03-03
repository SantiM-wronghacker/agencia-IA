#!/usr/bin/env python
"""Just start API fresh"""
# AREA: HERRAMIENTAS
# DESCRIPCION: Just start API fresh
# TECNOLOGIA: Python

import os
import sys
import subprocess
import time
import urllib.request
import json
import datetime

def main():
    # Start new API
    print("Starting API...")
    venv_python = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\Santi\agentes-local\.venv\Scripts\python.exe"
    api_file = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\Santi\agentes-local\api_agencia.py"
    timeout = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    host = sys.argv[4] if len(sys.argv) > 4 else 'localhost'
    port = int(sys.argv[5]) if len(sys.argv) > 5 else 8000

    # Try to start it (may fail if already running, that's ok)
    try:
        subprocess.Popen([venv_python, api_file], creationflags=0x00000008)  # DETACHED_PROCESS
        print("API process started in background")
    except Exception as e:
        print(f"Could not start API: {e}")

    # Wait for it to start
    time.sleep(4)

    # Test /test-19-cats
    print("\nTesting /test-19-cats endpoint...")
    try:
        response = urllib.request.urlopen(f'http://{host}:{port}/test-19-cats', timeout=timeout)
        data = json.load(response)
        print(f"✓ Success!")
        print(f"  Count: {data.get('count')}")
        print(f"  Categories count: {len(data.get('categorias', []))}")
        print(f"  First 3 categories: {data.get('categorias', [])[:3]}")
        print(f"  Last update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Response status: {response.status}")
        print(f"  Response reason: {response.reason}")
        print(f"  Response headers: {response.info()}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Also test /agentes-list
    print("\nTesting /agentes-list endpoint...")
    try:
        req = urllib.request.Request(f'http://{host}:{port}/agentes-list')
        req.add_header('Authorization', 'Bearer santi-agencia-2026')
        response = urllib.request.urlopen(req, timeout=timeout)
        data = json.load(response)
        print(f"✓ Success!")
        print(f"  Agentes: {len(data.get('agentes', {}))}")
        print(f"  Agentes por categoria: {data.get('agentes_por_categoria', {})}")
        print(f"  Ultima actualizacion: {data.get('ultima_actualizacion', '')}")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Resumen ejecutivo
    print("\nResumen ejecutivo:")
    print(f"  API started: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Host: {host}")
    print(f"  Port: {port}")
    print(f"  Timeout: {timeout} segundos")
    print(f"  Resultado /test-19-cats: {'Exitoso' if '✓ Success!' in sys.stdout.getvalue() else 'Fallido'}")
    print(f"  Resultado /agentes-list: {'Exitoso' if '✓ Success!' in sys.stdout.getvalue() else 'Fallido'}")

if __name__ == "__main__":
    main()