@echo off
chcp 65001 >nul
title Estado del Sistema — Agencia Santi
color 0E

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║        ESTADO DEL SISTEMA AGENCIA SANTI           ║
echo  ╚═══════════════════════════════════════════════════╝
echo.

cd /d C:\Users\Santi\agentes-local

REM Verificar si Python esta corriendo
tasklist /FI "IMAGENAME eq python.exe" 2>nul | find /I "python.exe" >nul
if !errorlevel! equ 0 (
    echo  [ESTADO] Python se esta ejecutando...
) else (
    echo  [ESTADO] Python NO se esta ejecutando.
)

echo.
echo  Verificando accesibilidad de servicios...
echo.

REM Verificar API
curl -s http://localhost:8000/docs >nul 2>&1
if !errorlevel! equ 0 (
    echo  [OK] API        - Accesible en http://localhost:8000
) else (
    echo  [X]  API        - NO ACCESIBLE
)

REM Verificar Dashboard
curl -s http://localhost:8080 >nul 2>&1
if !errorlevel! equ 0 (
    echo  [OK] Dashboard  - Accesible en http://localhost:8080
) else (
    echo  [X]  Dashboard  - NO ACCESIBLE
)

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║             OPCIONES DE MANTENIMIENTO             ║
echo  ╚═══════════════════════════════════════════════════╝
echo.
echo  1. Iniciar sistema (arrancar.bat)
echo  2. Ver ultimos logs (sistema_maestro.log)
echo  3. Matar procesos Python y limpiar
echo  4. Verificar expansion_plan.json
echo  5. Salir
echo.

set /p opcion="Selecciona una opcion [1-5]: "

if "%opcion%"=="1" (
    echo.
    echo  Iniciando arrancar.bat...
    call arrancar.bat
) else if "%opcion%"=="2" (
    echo.
    if exist sistema_maestro.log (
        echo  Ultimos 30 lineas del log:
        echo.
        for /f "skip=*" %%a in ('find /c /v "" ^< sistema_maestro.log') do set total=%%a
        set /a inicio=total-30
        if !inicio! lss 0 set inicio=0
        REM Simple tail simulation - mostrar ultimas lineas
        powershell -Command "Get-Content sistema_maestro.log | Select-Object -Last 30"
    ) else (
        echo  No se encontro el archivo de log.
    )
    echo.
    pause
    call estado_sistema.bat
) else if "%opcion%"=="3" (
    echo.
    echo  Matando procesos Python...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2 /nobreak >nul
    echo  [OK] Procesos terminados. Sistema limpio.
    echo.
    pause
    call estado_sistema.bat
) else if "%opcion%"=="4" (
    echo.
    if exist expansion_plan.json (
        echo  Verificando expansion_plan.json...
        python -c "import json; f=open('expansion_plan.json'); data=json.load(f); print(f'  Total planificado: {data.get(\"meta\", {}).get(\"total_planificados\", \"?\")}')" 2>nul || echo  (error al leer JSON)
    ) else (
        echo  No se encontro expansion_plan.json.
    )
    echo.
    pause
    call estado_sistema.bat
) else if "%opcion%"=="5" (
    echo.
    echo  Saliendo...
    timeout /t 1 /nobreak >nul
    exit /b 0
) else (
    echo.
    echo  Opcion invalida.
    timeout /t 2 /nobreak >nul
    call estado_sistema.bat
)
