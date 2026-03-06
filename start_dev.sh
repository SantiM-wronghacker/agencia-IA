#!/bin/bash
# ==========================================
# Script de arranque para desarrollo local
# ==========================================

set -e

echo "🚀 Arrancando Agencia IA (Desarrollo Local)"
echo "=========================================="

# Verificar Python
if ! command -v python &> /dev/null; then
    echo "❌ Python no encontrado. Instala Python 3.10+"
    exit 1
fi

# Crear venv si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando virtualenv..."
    python -m venv venv
fi

# Activar venv
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate

# Instalar deps
echo "📥 Instalando dependencias..."
pip install -q -r requirements.txt

# Crear .env.local si no existe
if [ ! -f ".env.local" ]; then
    echo "⚙️  Creando .env.local (copia de .env.example)..."
    cp .env.example .env.local
    echo "⚠️  EDITA .env.local y añade tu GROQ_API_KEY"
fi

# Cargar env
export $(cat .env.local | grep -v '^#' | xargs)

echo ""
echo "✅ Listo. Opciones:"
echo ""
echo "1️⃣  Correr TESTS:"
echo "   pytest tests/ -v"
echo ""
echo "2️⃣  Arrancar API:"
echo "   uvicorn src.agencia.api.api:app --reload --host 127.0.0.1 --port 8000"
echo ""
echo "3️⃣  Ejecutar agente:"
echo "   python -m agencia.agents.ventas.seguimiento_pipeline"
echo ""
echo "Para más info: cat DESARROLLO_LOCAL.md"
