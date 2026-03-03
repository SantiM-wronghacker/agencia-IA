@echo off
chcp 65001 >nul
title Agencia Santi — Sistema Maestro
color 0A
setlocal enabledelayedexpansion

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║     AGENCIA SANTI — INICIANDO SISTEMA COMPLETO    ║
echo  ║              Dashboard + API + Agentes            ║
echo  ╚═══════════════════════════════════════════════════╝
echo.

cd /d C:\Users\Santi\agentes-local

REM Paso 1: Limpiar procesos antiguos
echo  [1/5] Limpiando procesos anteriores...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Sistema Maestro*" 2>nul
timeout /t 1 /nobreak >nul

REM Paso 2: Activar venv
echo  [2/5] Activando entorno virtual...
call .venv\Scripts\activate.bat 2>nul || echo  (sin venv, usando Python global)

REM Paso 3: Verificar dependencias
echo  [3/5] Verificando dependencias...
python -c "import groq, dotenv, cerebras, mistralai, google.genai" 2>nul || pip install groq python-dotenv cerebras-cloud-sdk mistralai google-genai --quiet

REM Paso 4: Iniciar Sistema Maestro en background
echo  [4/5] Iniciando Sistema Maestro en segundo plano...
start /B python sistema_maestro.py > sistema_maestro.log 2>&1
timeout /t 3 /nobreak >nul

REM Paso 5: Verificar que API respondea y abrir dashboard
echo  [5/5] Verificando accesibilidad de API y dashboard...
set "contador=0"
:esperar_api
curl -s http://localhost:8000/docs >nul 2>&1
if !errorlevel! equ 0 (
    echo.
    echo  [OK] Sistema listo. Abriendo dashboard en navegador...
    timeout /t 2 /nobreak >nul
    start http://localhost:8080
    echo.
    echo  ╔═══════════════════════════════════════════════════╗
    echo  ║    SISTEMA ACTIVO                                 ║
    echo  ║                                                   ║
    echo  ║  Dashboard:  http://localhost:8080                ║
    echo  ║  API:        http://localhost:8000                ║
    echo  ║  API Docs:   http://localhost:8000/docs           ║
    echo  ║                                                   ║
    echo  ║  Sistema ejecutandose en segundo plano.           ║
    echo  ║  Para ver logs, abre: sistema_maestro.log         ║
    echo  ╚═══════════════════════════════════════════════════╝
    echo.
    pause
    exit /b 0
)

REM Si no responde, reintentar hasta 30 segundos
set /a contador=!contador!+1
if !contador! lss 30 (
    timeout /t 1 /nobreak >nul
    goto esperar_api
)

REM Si API no responde después de 30 segundos
echo.
echo  [ERROR] El API no respondio dentro de 30 segundos.
echo  Verifica el log: sistema_maestro.log
echo.
pause
exit /b 1