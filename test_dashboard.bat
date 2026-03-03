@echo off
REM Test script para verificar que el dashboard funciona

echo ============================================
echo TEST: Dashboard Standalone Integration
echo ============================================
echo.

REM Verificar que existen los archivos necesarios
echo [1/3] Verificando archivos...
if exist "dashboard_standalone.html" (
    echo   ✓ dashboard_standalone.html existe
) else (
    echo   ✗ ERROR: dashboard_standalone.html NO existe
    pause
    exit /b 1
)

if exist "api_agencia.py" (
    echo   ✓ api_agencia.py existe
) else (
    echo   ✗ ERROR: api_agencia.py NO existe
    pause
    exit /b 1
)

echo.
echo [2/3] Verificando sintaxis Python...
python -m py_compile api_agencia.py >nul 2>&1
if %errorlevel% equ 0 (
    echo   ✓ Sintaxis de Python correcta
) else (
    echo   ✗ ERROR: Sintaxis inválida
    pause
    exit /b 1
)

echo.
echo [3/3] Iniciando servidor...
echo   → Abriendo en: http://localhost:8000/dashboard
echo   → Acceso remoto: http://<tu-IP>:8000/dashboard
echo.
echo   Presiona Ctrl+C en esta ventana para detener el servidor
echo.

timeout /t 2 /nobreak
python api_agencia.py
