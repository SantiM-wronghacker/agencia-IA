@echo off
REM ==========================================
REM Script de arranque para desarrollo local
REM Windows
REM ==========================================

echo.
echo 🚀 Arrancando Agencia IA (Desarrollo Local)
echo ==========================================

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no encontrado. Instala Python 3.10+
    pause
    exit /b 1
)

REM Crear venv si no existe
if not exist "venv" (
    echo 📦 Creando virtualenv...
    python -m venv venv
)

REM Activar venv
call venv\Scripts\activate.bat

REM Instalar deps
echo 📥 Instalando dependencias...
pip install -q -r requirements.txt

REM Crear .env.local si no existe
if not exist ".env.local" (
    echo ⚙️  Creando .env.local (copia de .env.example)...
    copy .env.example .env.local
    echo ⚠️  EDITA .env.local y añade tu GROQ_API_KEY
)

REM Cargar env (Windows no lo hace automático)
echo.
echo ✅ Listo. Opciones:
echo.
echo 1️⃣  Correr TESTS:
echo    pytest tests/ -v
echo.
echo 2️⃣  Arrancar API:
echo    uvicorn src.agencia.api.api:app --reload --host 127.0.0.1 --port 8000
echo.
echo 3️⃣  Ejecutar agente:
echo    python -m agencia.agents.ventas.seguimiento_pipeline
echo.
echo Para más info: type DESARROLLO_LOCAL.md
echo.
pause
