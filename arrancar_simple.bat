@echo off
setlocal enabledelayedexpansion

REM Configurar directorio
cd /d "%~dp0"

REM Limpiar procesos previos
echo [1/3] Limpiando procesos previos...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak

REM Iniciar API (incluye dashboard)
echo [2/3] Iniciando API + Dashboard (puerto 8000)...
start "API AGENCIA" /min python api_agencia.py
timeout /t 3 /nobreak

REM Abrir navegador
echo [3/3] Abriendo dashboard en navegador...
timeout /t 2 /nobreak
start http://localhost:8000/dashboard

echo.
echo ============================================
echo API:       http://localhost:8000/status
echo DASHBOARD: http://localhost:8000/dashboard
echo Acceso remoto: http://<IP>:8000/dashboard
echo ============================================
echo.
echo Para detener: Cierra las ventanas de "API AGENCIA" y "DASHBOARD"
echo.
pause
