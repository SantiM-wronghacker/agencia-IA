@echo off
chcp 65001 >nul
title Abrir Dashboard — Agencia Santi

cd /d C:\Users\Santi\agentes-local

echo.
echo  Verificando que el sistema este activo...

REM Verificar si API responde
curl -s http://localhost:8000/docs >nul 2>&1

if !errorlevel! equ 0 (
    echo  [OK] Sistema activo. Abriendo dashboard...
    timeout /t 1 /nobreak >nul
    start http://localhost:8080
    echo.
    echo  Dashboard abierto en: http://localhost:8080
    echo.
) else (
    echo  [ERROR] El sistema NO esta activo.
    echo.
    echo  Necesitas iniciar el sistema primero:
    echo  1. Abre arrancar.bat para iniciar todo
    echo  2. O ejecuta: estado_sistema.bat
    echo.
    pause
)
