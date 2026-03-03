@echo off
chcp 65001 >nul
title Configurar Auto-inicio — Agencia Santi
color 0B

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║      CONFIGURAR AUTO-INICIO DEL SISTEMA           ║
echo  ║   (El sistema se iniciara automaticamente         ║
echo  ║    cada vez que enciendes tu computadora)         ║
echo  ╚═══════════════════════════════════════════════════╝
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo  [ERROR] Este script requiere permisos de ADMINISTRADOR.
    echo
    echo  Solucion:
    echo  1. Abre CMD como Administrador
    echo  2. Ejecuta: activar_autostart.bat
    echo.
    pause
    exit /b 1
)

cd /d C:\Users\Santi\agentes-local

echo  Creando tarea programada en Windows Task Scheduler...
echo.

REM Crear la tarea programada
schtasks /create /tn "Agencia Santi - Sistema Maestro" ^
    /tr "cmd.exe /c start /B python sistema_maestro.py" ^
    /sc onlogon ^
    /rl highest ^
    /f 2>nul

if !errorlevel! equ 0 (
    echo.
    echo  [OK] Tarea creada exitosamente.
    echo.
    echo  El sistema ahora se iniciara automaticamente cuando:
    echo  - Enciendas tu computadora
    echo  - Inicies sesion en Windows
    echo.
    echo  Para dejar de usar auto-inicio, ejecuta:
    echo  > desactivar_autostart.bat
    echo.
) else (
    echo.
    echo  [ERROR] No se pudo crear la tarea programada.
    echo.
)

pause
