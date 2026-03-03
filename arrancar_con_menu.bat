@echo off
chcp 65001 >nul
title Agencia Santi — Selector de Prioridades
color 0B
setlocal enabledelayedexpansion

:menu
cls
echo.
echo  ╔═════════════════════════════════════════════════════╗
echo  ║     AGENCIA SANTI — SELECTOR DE PRIORIDADES        ║
echo  ║                                                     ║
echo  ║  Que quieres que haga el sistema?                  ║
echo  ╚═════════════════════════════════════════════════════╝
echo.
echo  1. CREAR - Generar nuevos agentes hasta 500
echo     (Fábrica: CREAR | Factory mode: CREATE)
echo.
echo  2. MEJORAR - Optimizar los 304 agentes existentes
echo     (Fábrica: MEJORAR | Factory mode: IMPROVE)
echo.
echo  3. BALANCEADO - Crear y mejorar simultáneamente
echo     (Fábrica: BALANCEADO | 60% crear, 40% mejorar)
echo.
echo  4. EXPANSION SOLO - Crear solo los 206 micros del plan
echo     (Ignora otros agentes, enfoque 100% en micros)
echo.
echo  5. NOCHE COMPLETA - Todas las tareas (noche, misiones, etc)
echo     (Default: factory + night mode + auto-run)
echo.
echo  ─────────────────────────────────────────────────────
set /p opcion="Selecciona [1-5] (default: 5): "

if "%opcion%"=="" set opcion=5

if "%opcion%"=="1" (
    set modo=CREAR
    set desc=Modo CREAR activado: generar nuevos agentes
) else if "%opcion%"=="2" (
    set modo=MEJORAR
    set desc=Modo MEJORAR activado: optimizar agentes existentes
) else if "%opcion%"=="3" (
    set modo=BALANCEADO
    set desc=Modo BALANCEADO: crear Y mejorar
) else if "%opcion%"=="4" (
    set modo=EXPANSION
    set desc=Modo EXPANSION: solo los 206 micros planificados
) else if "%opcion%"=="5" (
    set modo=NOCHE
    set desc=Modo NOCHE COMPLETA: todas las tareas
) else (
    echo  [ERROR] Opcion invalida.
    timeout /t 2 /nobreak >nul
    goto menu
)

REM Guardar la preferencia en un archivo config
echo %modo% > .fabricamode

echo.
echo  [OK] %desc%
echo  Iniciando sistema...
echo.
timeout /t 2 /nobreak >nul

REM Ahora llamar al arrancar normal
call arrancar.bat
