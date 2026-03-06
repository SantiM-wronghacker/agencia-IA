#!/bin/bash
# ==========================================
# Arrancar servicios con Podman
# ==========================================

set -e

echo "🐳 Arrancando Podman..."

# Verificar si Podman está instalado
if ! command -v podman &> /dev/null; then
    echo "❌ Podman no instalado"
    echo "Instala con: brew install podman"
    exit 1
fi

# Arrancar máquina Podman (Mac)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📍 Iniciando máquina Podman (Mac)..."
    podman machine start 2>/dev/null || true
    sleep 2
fi

# Verificar que Podman está disponible
if ! podman ps &> /dev/null; then
    echo "❌ Podman no responde"
    exit 1
fi

# Arrancar docker-compose con Podman
echo "🚀 Arrancando servicios..."
podman-compose -f docker-compose.yml up -d

# Esperar a que Elasticsearch esté listo
echo "⏳ Esperando Elasticsearch..."
for i in {1..30}; do
    if curl -s http://localhost:9200/_cluster/health &> /dev/null; then
        echo "✅ Elasticsearch listo"
        break
    fi
    sleep 1
done

echo ""
echo "✅ Servicios iniciados con Podman:"
echo ""
podman ps --format "table {{.Names}}\t{{.Ports}}\t{{.Status}}"

echo ""
echo "📊 URLs de acceso:"
echo "  Elasticsearch: http://localhost:9200"
echo "  Kibana:        http://localhost:5601"
echo "  Redis:         localhost:6379"
echo "  Prometheus:    http://localhost:9090"
echo "  Grafana:       http://localhost:3000"
echo "  Jaeger:        http://localhost:16686"
echo ""
echo "🛑 Para detener: podman-compose down"
