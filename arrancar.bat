@echo off
chcp 65001 >nul
title Agencia Santi — Sistema Maestro
color 0A
echo.
echo  ╔══════════════════════════════════════════╗
echo  ║    AGENCIA SANTI — INICIANDO SISTEMA     ║
echo  ╚══════════════════════════════════════════╝
echo.
cd /d C:\Users\Santi\agentes-local
echo  [1/3] Activando entorno virtual...
call .venv\Scripts\activate.bat 2>nul || echo  (sin venv, usando Python global)
echo  [2/3] Verificando dependencias...
python -c "import groq, dotenv, cerebras, mistralai, google.genai" 2>nul || pip install groq python-dotenv cerebras-cloud-sdk mistralai google-genai --quiet
echo  [3/3] Arrancando Sistema Maestro...
echo.
python sistema_maestro.py
pause