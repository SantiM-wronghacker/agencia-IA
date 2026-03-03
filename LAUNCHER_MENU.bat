@echo off
chcp 65001 >nul
title Menu Launcher — Agencia Santi
color 0F

:menu
cls
echo.
echo  ╔═════════════════════════════════════════════════╗
echo  ║      AGENCIA SANTI — MENU PRINCIPAL             ║
echo  ║       Dashboard + API + Sistema Maestro         ║
echo  ╚═════════════════════════════════════════════════╝
echo.
echo  OPCIONES:
echo  ─────────────────────────────────────────────────
echo.
echo  1.  Iniciar SISTEMA COMPLETO
echo      (API + Dashboard + Agentes)
echo.
echo  2.  Abrir DASHBOARD (si sistema ya está corriendo)
echo.
echo  3.  Ver ESTADO DEL SISTEMA
echo      (API, Dashboard, procesos, logs)
echo.
echo  4.  Configurar AUTO-INICIO
echo      (Sistema se inicia automáticamente al boot)
echo.
echo  5.  Desactivar AUTO-INICIO
echo      (Volver a inicio manual)
echo.
echo  6.  Ver LOGS (ultimas 50 lineas)
echo.
echo  7.  Limpiar PROCESOS
echo      (Mata todos los python y limpia)
echo.
echo  8.  Abrir CARPETA DEL PROYECTO
echo.
echo  9.  Abrir GUIA DE ARRANQUE
echo.
echo  0.  SALIR
echo.
echo  ─────────────────────────────────────────────────
set /p opcion="Selecciona una opcion [0-9]: "

if "%opcion%"=="1" call arrancar.bat & goto menu
if "%opcion%"=="2" call abrir_dashboard.bat & goto menu
if "%opcion%"=="3" call estado_sistema.bat & goto menu
if "%opcion%"=="4" call activar_autostart.bat & goto menu
if "%opcion%"=="5" call desactivar_autostart.bat & goto menu

if "%opcion%"=="6" (
    cls
    echo.
    echo  Ultimas 50 lineas del log:
    echo  ─────────────────────────────────────────────────
    echo.
    if exist sistema_maestro.log (
        powershell -Command "Get-Content sistema_maestro.log | Select-Object -Last 50"
    ) else (
        echo  (Log aun no creado. Inicia el sistema primero con opcion 1)
    )
    echo.
    pause
    goto menu
)

if "%opcion%"=="7" (
    echo.
    echo  Matando procesos Python...
    taskkill /F /IM python.exe 2>nul
    timeout /t 2 /nobreak >nul
    echo  [OK] Procesos terminados. Sistema limpio.
    echo.
    pause
    goto menu
)

if "%opcion%"=="8" (
    explorer.exe C:\Users\Santi\agentes-local
    goto menu
)

if "%opcion%"=="9" (
    cls
    echo.
    if exist GUIA_ARRANQUE.txt (
        type GUIA_ARRANQUE.txt
    ) else (
        echo  (Archivo GUIA_ARRANQUE.txt no encontrado)
    )
    echo.
    pause
    goto menu
)

if "%opcion%"=="0" (
    echo.
    echo  Adios...
    timeout /t 1 /nobreak >nul
    exit /b 0
)

echo.
echo  Opcion invalida.
timeout /t 2 /nobreak >nul
goto menu
