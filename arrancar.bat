@echo off
chcp 65001 >nul
title Agencia Santi — Sistema Maestro v2
color 0A
setlocal enabledelayedexpansion

echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║   AGENCIA SANTI — SISTEMA MAESTRO v2.0              ║
echo  ║   Director AI  ·  510 Agentes  ·  LLM Multi-Provider ║
echo  ╚══════════════════════════════════════════════════════╝
echo.

cd /d C:\Users\Santi\agentes-local

REM ─── PASO 1: Limpiar procesos previos ────────────────────────────────────
echo  [1/6] Limpiando procesos anteriores...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Sistema Maestro*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Agencia Santi*" 2>nul
timeout /t 1 /nobreak >nul

REM ─── PASO 2: Activar entorno virtual ─────────────────────────────────────
echo  [2/6] Activando entorno virtual...
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat 2>nul
    echo        OK: .venv activado
) else (
    echo        AVISO: .venv no encontrado, usando Python global
)

REM ─── PASO 3: Verificar Python y dependencias ──────────────────────────────
echo  [3/6] Verificando Python y dependencias criticas...
python --version 2>nul || (
    echo        ERROR: Python no encontrado en PATH
    pause & exit /b 1
)
python -c "import groq" 2>nul || (
    echo        Instalando dependencias LLM...
    pip install groq python-dotenv cerebras-cloud-sdk mistralai google-genai --quiet
)

REM ─── PASO 4: Verificar archivos clave ────────────────────────────────────
echo  [4/6] Verificando archivos del proyecto...
if not exist "sistema_maestro.py" (
    echo        ERROR: sistema_maestro.py no encontrado
    pause & exit /b 1
)
if not exist "habilidades.json" (
    echo        AVISO: habilidades.json no encontrado en raiz
) else (
    for /f %%i in ('python -c "import json;d=json.load(open(chr(34)+'habilidades.json'+chr(34)));print(len(d))" 2^>nul') do (
        echo        OK: %%i agentes cargados desde habilidades.json
    )
)
if exist ".env" (
    echo        OK: .env encontrado con variables de entorno
) else (
    echo        AVISO: .env no encontrado — crea uno con tus API keys
)

REM ─── PASO 5: Iniciar Sistema Maestro ─────────────────────────────────────
echo  [5/6] Iniciando Sistema Maestro en segundo plano...
start "Agencia Santi - Sistema Maestro" /B python sistema_maestro.py > sistema_maestro.log 2>&1
echo        PID iniciado — logs en: sistema_maestro.log
timeout /t 4 /nobreak >nul

REM ─── PASO 6: Health checks ───────────────────────────────────────────────
echo  [6/6] Verificando servicios...
echo.

set "api_ok=0"
set "dash_ok=0"
set "contador=0"

:health_loop
set /a contador=!contador!+1

REM Verificar API (puerto 8000)
if "!api_ok!"=="0" (
    curl -s --max-time 2 http://localhost:8000/ >nul 2>&1
    if !errorlevel! equ 0 (
        set "api_ok=1"
        echo       API  OK  http://localhost:8000
    ) else (
        echo       API  ...  Intento !contador!/60 esperando...
    )
)

REM Verificar Dashboard (puerto 8080)
if "!dash_ok!"=="0" (
    curl -s --max-time 2 http://localhost:8080/ >nul 2>&1
    if !errorlevel! equ 0 (
        set "dash_ok=1"
        echo       WEB  OK  http://localhost:8080
    )
)

REM Ambos servicios listos?
if "!api_ok!"=="1" if "!dash_ok!"=="1" goto :servicios_listos

REM Timeout?
if !contador! geq 60 goto :timeout_error

timeout /t 1 /nobreak >nul
goto :health_loop

:servicios_listos
echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║   SISTEMA ACTIVO — TODOS LOS SERVICIOS OK           ║
echo  ╠══════════════════════════════════════════════════════╣
echo  ║                                                      ║
echo  ║   Dashboard:    http://localhost:8080                ║
echo  ║   API REST:     http://localhost:8000                ║
echo  ║   API Status:   http://localhost:8000/status         ║
echo  ║   Director AI:  POST /director/asignar               ║
echo  ║                                                      ║
echo  ║   Logs:         sistema_maestro.log                  ║
echo  ║                                                      ║
echo  ╚══════════════════════════════════════════════════════╝
echo.
timeout /t 2 /nobreak >nul
start http://localhost:8080
echo  Navegador abierto en Dashboard. Presiona cualquier tecla para salir.
echo  (el sistema continua ejecutandose en segundo plano)
echo.
pause
exit /b 0

:timeout_error
echo.
echo  ╔══════════════════════════════════════════════════════╗
echo  ║   ERROR — Servicios no respondieron en 60 segundos  ║
echo  ╠══════════════════════════════════════════════════════╣
if "!api_ok!"=="0" (
echo  ║   API (8000):       NO RESPONDE                      ║
) else (
echo  ║   API (8000):       OK                               ║
)
if "!dash_ok!"=="0" (
echo  ║   Dashboard (8080): NO RESPONDE                      ║
) else (
echo  ║   Dashboard (8080): OK                               ║
)
echo  ╠══════════════════════════════════════════════════════╣
echo  ║   Revisa: sistema_maestro.log                        ║
echo  ║   O corre manualmente:                               ║
echo  ║     python api_agencia.py                            ║
echo  ║     python dashboard_web.py                          ║
echo  ╚══════════════════════════════════════════════════════╝
echo.
pause
exit /b 1
