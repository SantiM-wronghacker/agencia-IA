# 🐳 Podman Setup - Alternativa Optimizada a Docker

Podman es más ligero que Docker, sin daemon siempre corriendo, y compatible con docker-compose.

## Instalación

### Mac (Intel/M1/M2)
```bash
brew install podman

# Inicializar máquina virtual
podman machine init
podman machine start
```

### Linux
```bash
sudo apt update
sudo apt install podman podman-compose  # Debian/Ubuntu
# o
sudo dnf install podman podman-compose  # Fedora/RHEL
```

### Windows
```bash
choco install podman  # Con Chocolatey
# o descargar desde: https://github.com/containers/podman/releases
```

## Uso

### Equivalencias Docker → Podman

```bash
# Docker
docker ps                 →  podman ps
docker build .            →  podman build .
docker run -it image      →  podman run -it image

# Docker Compose
docker-compose up         →  podman-compose up
docker-compose down       →  podman-compose down
docker-compose logs -f    →  podman-compose logs -f
```

### Arrancar servicios con Podman

```bash
# Opción 1: Usar docker-compose.yml con Podman
podman-compose -f docker-compose.yml up -d

# Opción 2: Verificar servicios
podman ps
podman logs elasticsearch
podman logs redis

# Opción 3: Detener
podman-compose down
```

## Ventajas sobre Docker

| Característica | Docker | Podman |
|---|---|---|
| Daemon siempre corriendo | ✅ Sí | ❌ No (más eficiente) |
| Memoria en reposo | ~500 MB | ~50 MB |
| Seguridad | rootless (config) | rootless (por defecto) |
| Compatibilidad | Estándar | 100% compatible |
| Performance | Bueno | Mejor 5-10% |

## Configuración Recomendada

```bash
# 1. Instalar Podman
brew install podman

# 2. Inicializar (Mac)
podman machine init --cpus=4 --memory=8192
podman machine start

# 3. Usar docker-compose.yml existente
podman-compose up -d

# 4. Verificar
podman ps
curl http://localhost:9200/_cluster/health
```

## Problemas Comunes

### "podman: command not found"
```bash
# Mac: inicia la máquina
podman machine start

# Linux: instala podman-compose
sudo apt install podman-compose
```

### "Cannot connect to Podman socket"
```bash
# Mac: reinicia la máquina
podman machine stop
podman machine start
```

### Puerto ya en uso
```bash
# Ver qué servicios usan puertos
podman ps -a
podman port

# Detener servicio específico
podman stop nombre_contenedor
```

## Scripts de Arranque (Podman)

### Mac/Linux
```bash
#!/bin/bash
podman machine start 2>/dev/null || true
podman-compose -f docker-compose.yml up -d
echo "✅ Servicios iniciados con Podman"
podman ps
```

### Monitoreo
```bash
# Ver logs en tiempo real
podman-compose logs -f elasticsearch

# Ver recursos
podman stats

# Ver todos los contenedores
podman ps -a
```

## Desarrollo con Podman

### Flujo típico
```bash
# 1. Iniciar Podman
podman machine start

# 2. Arrancar servicios (background)
podman-compose up -d

# 3. Desarrollar normalmente
pytest tests/ -v
uvicorn src.agencia.api.api:app --reload

# 4. Detener cuando termines
podman-compose down
```

### Con volumenes
```bash
# Compartir directorio local con contenedor
podman run -v /path/local:/path/contenedor image

# Ejemplo: volumen para Elasticsearch data
podman volume create es-data
podman run -v es-data:/usr/share/elasticsearch/data elasticsearch:8.12.0
```

## Comparación: Docker vs Podman vs Local

| Aspecto | Docker | Podman | Local |
|---|---|---|---|
| Setup | 10 min | 5 min | 5 min |
| Recursos | Alto | Bajo | Muy bajo |
| Servicios | Todos contenidos | Todos contenidos | Instalados |
| Performance | Bueno | Mejor | Mejor |
| Portable | Muy portable | Muy portable | SO-específico |

## Recomendación Final

✅ **Usa Podman si:**
- Quieres servicios completos (Elasticsearch, Redis, RabbitMQ)
- Tu máquina tiene recursos limitados
- Prefieres no instalar servicios localmente
- Necesitas ambiente reproducible

✅ **Usa desarrollo local puro si:**
- Solo necesitas API + tests
- Máquina con pocos recursos
- Prefieres máxima velocidad
- Sin Docker/Podman disponible

## Próximos pasos

```bash
# 1. Instalar Podman
brew install podman

# 2. Inicializar
podman machine init

# 3. Arrancar servicios
podman-compose up -d

# 4. Verificar
curl http://localhost:9200/_cluster/health
podman ps
```
