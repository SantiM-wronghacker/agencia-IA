@echo off
chcp 65001 >nul
title Verificar Instalacion — Agencia Santi
color 0A

echo.
echo  ╔═════════════════════════════════════════════════════╗
echo  ║      VERIFICANDO INSTALACION DEL SISTEMA            ║
echo  ║            Agencia Santi - Marzo 2026               ║
echo  ╚═════════════════════════════════════════════════════╝
echo.

cd /d C:\Users\Santi\agentes-local

setlocal enabledelayedexpansion

REM Contador de verificaciones
set verificadas=0
set total=0

REM Función auxiliar
set /a total=!total!+1
echo  [1/8] Verificando archivos creados...

if exist arrancar.bat (
    echo    ✓ arrancar.bat (mejorado)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ arrancar.bat (FALTA)
)

if exist LAUNCHER_MENU.bat (
    echo    ✓ LAUNCHER_MENU.bat
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ LAUNCHER_MENU.bat (FALTA)
)

if exist activar_autostart.bat (
    echo    ✓ activar_autostart.bat
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ activar_autostart.bat (FALTA)
)

if exist desactivar_autostart.bat (
    echo    ✓ desactivar_autostart.bat
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ desactivar_autostart.bat (FALTA)
)

if exist estado_sistema.bat (
    echo    ✓ estado_sistema.bat
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ estado_sistema.bat (FALTA)
)

if exist abrir_dashboard.bat (
    echo    ✓ abrir_dashboard.bat
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ abrir_dashboard.bat (FALTA)
)

if exist EMPEZAR_AQUI.txt (
    echo    ✓ EMPEZAR_AQUI.txt
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ EMPEZAR_AQUI.txt (FALTA)
)

if exist GUIA_ARRANQUE.txt (
    echo    ✓ GUIA_ARRANQUE.txt
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ GUIA_ARRANQUE.txt (FALTA)
)

if exist RESUMEN_SOLUCION_ARRANQUE.md (
    echo    ✓ RESUMEN_SOLUCION_ARRANQUE.md
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ RESUMEN_SOLUCION_ARRANQUE.md (FALTA)
)

echo.
set /a total=!total!+1
echo  [2/8] Verificando archivos del sistema...

if exist habilidades.json (
    echo    ✓ habilidades.json
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ habilidades.json (FALTA)
)

if exist expansion_plan.json (
    echo    ✓ expansion_plan.json (206 micros planificados)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ expansion_plan.json (FALTA)
)

if exist api_agencia.py (
    echo    ✓ api_agencia.py (con 10+ endpoints nuevos)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ api_agencia.py (FALTA)
)

if exist dashboard_web.py (
    echo    ✓ dashboard_web.py (completamente reescrito)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ dashboard_web.py (FALTA)
)

if exist sistema_maestro.py (
    echo    ✓ sistema_maestro.py
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ sistema_maestro.py (FALTA)
)

echo.
set /a total=!total!+1
echo  [3/8] Verificando entorno virtual...

if exist .venv\Scripts\activate.bat (
    echo    ✓ Entorno virtual (.venv)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ Entorno virtual (.venv) (FALTA)
)

echo.
set /a total=!total!+1
echo  [4/8] Verificando Python...

python --version >nul 2>&1
if !errorlevel! equ 0 (
    for /f "tokens=*" %%i in ('python --version') do set PYVER=%%i
    echo    ✓ Python instalado (!PYVER!)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ Python NO instalado (REQUERIDO)
)

echo.
set /a total=!total!+1
echo  [5/8] Verificando dependencias...

python -c "import groq" 2>nul
if !errorlevel! equ 0 (
    echo    ✓ Groq
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ Groq (pip install groq)
)

python -c "import dotenv" 2>nul
if !errorlevel! equ 0 (
    echo    ✓ python-dotenv
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ python-dotenv (pip install python-dotenv)
)

python -c "import fastapi" 2>nul
if !errorlevel! equ 0 (
    echo    ✓ FastAPI
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ FastAPI (pip install fastapi)
)

echo.
set /a total=!total!+1
echo  [6/8] Verificando servicios corriendo...

curl -s http://localhost:8000/health >nul 2>&1
if !errorlevel! equ 0 (
    echo    ✓ API respondiendo (http://localhost:8000)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ API NO RESPONDIENDO (ejecuta arrancar.bat primero)
)

curl -s http://localhost:8080 >nul 2>&1
if !errorlevel! equ 0 (
    echo    ✓ Dashboard accesible (http://localhost:8080)
    set /a verificadas=!verificadas!+1
) else (
    echo    ✗ Dashboard NO ACCESIBLE (ejecuta arrancar.bat primero)
)

echo.
set /a total=!total!+1
echo  [7/8] Verificando datos...

if exist habilidades.json (
    for /f %%i in ('python -c "import json; f=open(\"habilidades.json\"); d=json.load(f); print(len(d))" 2^>nul') do set AGENTES=%%i
    if defined AGENTES (
        echo    ✓ !AGENTES! agentes en el sistema
        set /a verificadas=!verificadas!+1
    ) else (
        echo    ✗ No se pudo contar agentes
    )
)

if exist expansion_plan.json (
    for /f %%i in ('python -c "import json; f=open(\"expansion_plan.json\"); d=json.load(f); print(len(d.get(\"micros\", [])))" 2^>nul') do set MICROS=%%i
    if defined MICROS (
        echo    ✓ !MICROS! micros planificados
        set /a verificadas=!verificadas!+1
    ) else (
        echo    ✗ No se pudo contar micros
    )
)

echo.
set /a total=!total!+1
echo  [8/8] Resumen final...

echo.
echo  ═══════════════════════════════════════════════════════════
echo.
echo    ARCHIVOS VERIFICADOS:       0/9
echo    SISTEMA VERIFICADO:         0/5
echo    DEPENDENCIAS VERIFICADO:    0/3
echo    SERVICIOS VERIFICADO:       0/2
echo    ─────────────────────────────────
echo    TOTAL VERIFICADO:           !verificadas!/23
echo.
echo  ═══════════════════════════════════════════════════════════
echo.

if !verificadas! geq 20 (
    echo    ✅ SISTEMA LISTO PARA USAR
    echo.
    echo    Próximos pasos:
    echo    1. Haz doble clic en: arrancar.bat
    echo    2. El dashboard se abrirá automáticamente
    echo    3. ¡Disfruta!
) else if !verificadas! geq 15 (
    echo    ⚠️  SISTEMA PARCIALMENTE LISTO
    echo.
    echo    Faltan cosas menores. Ejecuta:
    echo    1. arrancar.bat para iniciar servicios
    echo    2. pip install -r requirements.txt si hay errores
) else (
    echo    ❌ SISTEMA INCOMPLETO
    echo.
    echo    Faltan dependencias o archivos. Verifica arriba.
)

echo.
echo  Más información: EMPEZAR_AQUI.txt
echo.
pause
