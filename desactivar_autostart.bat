@echo off
chcp 65001 >nul
title Desactivar Auto-inicio — Agencia Santi
color 0C

echo.
echo  ╔═══════════════════════════════════════════════════╗
echo  ║     DESACTIVAR AUTO-INICIO DEL SISTEMA            ║
echo  ║   El sistema NO se iniciara mas automaticamente   ║
echo  ╚═══════════════════════════════════════════════════╝
echo.

REM Verificar permisos de administrador
net session >nul 2>&1
if !errorlevel! neq 0 (
    echo.
    echo  [ERROR] Este script requiere permisos de ADMINISTRADOR.
    echo.
    echo  Solucion:
    echo  1. Abre CMD como Administrador
    echo  2. Ejecuta: desactivar_autostart.bat
    echo.
    pause
    exit /b 1
)

echo  Eliminando tarea programada en Windows Task Scheduler...
echo.

REM Eliminar la tarea programada
schtasks /delete /tn "Agencia Santi - Sistema Maestro" /f 2>nul

if !errorlevel! equ 0 (
    echo.
    echo  [OK] Tarea eliminada exitosamente.
    echo.
    echo  El sistema ya NO se iniciara automaticamente.
    echo.
    echo  Puedes seguir iniciando manualmente con:
    echo  > arrancar.bat
    echo.
) else (
    echo.
    echo  [ERROR] No se pudo eliminar la tarea programada.
    echo  Probablemente no existia o ya fue eliminada.
    echo.
)

pause
