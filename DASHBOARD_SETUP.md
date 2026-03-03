# Dashboard Standalone - Setup Completado ✅

## Cambios Realizados

### 1. **dashboard_standalone.html** (Nuevo)
- Dashboard auto-contenido (HTML + CSS + JS en un solo archivo)
- No requiere servidor separado
- Se conecta directamente a API en puerto 8000
- Actualiza cada 10 segundos sin bloquear
- Métricas mostradas:
  - Estado del API (Online/Offline)
  - Total de agentes
  - Agentes saludables
  - Microagentes (206/206)
  - Categorías activas
  - Modo actual de fábrica
- Tabla de categorías con breakdown por "OK"
- Log de últimas actividades del sistema

### 2. **api_agencia.py** (Modificado)
- Nueva ruta pública `/dashboard` y `/dashboard.html`
- Sirve el archivo HTML directamente (sin auth requerida)
- Headers CORS configurados para acceso remoto
- Content-Type correcto: `text/html; charset=utf-8`

### 3. **arrancar_simple.bat** (Actualizado)
- Ahora solo inicia `api_agencia.py` (no necesita `dashboard_web.py`)
- Abre dashboard automáticamente en navegador local
- Simplificado de 4 pasos a 3 pasos

## Cómo Usar

### Opción 1: Desde tu computadora (localhost)
```
1. Ejecuta: C:\Users\Santi\agentes-local\arrancar_simple.bat
2. Se abrirá automáticamente: http://localhost:8000/dashboard
3. El dashboard muestra estado en tiempo real (actualiza cada 10s)
```

### Opción 2: Desde otro dispositivo (IP remoto)
```
1. En tu computadora:
   - Ejecuta arrancar_simple.bat
   - En command prompt: ipconfig
   - Busca la dirección IPv4 (ej: 192.168.1.100)

2. En otro dispositivo (teléfono, tablet, otra PC):
   - Abre navegador: http://192.168.1.100:8000/dashboard
   - Verás el mismo dashboard con datos en tiempo real
```

### Opción 3: Acceso directo a API
```
GET  http://localhost:8000/status         → Estado general
GET  http://localhost:8000/categorias     → Breakdown por categoría
GET  http://localhost:8000/expansion      → Progreso de expansión
GET  http://localhost:8000/modo           → Modo actual
```

## Ventajas del Nuevo Sistema

✅ **Sin dependencias externas**: Solo necesita Python (ya instalado)
✅ **Acceso remoto inmediato**: Desde cualquier dispositivo en la red
✅ **Sin procesos conflictivos**: Una sola instancia de Python (api_agencia.py)
✅ **No bloquea el inicio**: Dashboard actualiza async sin esperar respuesta
✅ **Muy ligero**: 6.1 KB de HTML (se carga instantáneamente)
✅ **No necesita configuración**: Funciona automáticamente
✅ **Resiliente**: Si hay error de API, muestra "Offline" pero sigue intentando

## Troubleshooting

### Dashboard muestra "Conectando..." indefinidamente
- Verifica que puerto 8000 está libre: `netstat -ano | findstr :8000`
- Si está ocupado, ejecuta: `limpiar_sistema.bat` y luego `arrancar_simple.bat`

### No puedo acceder desde otro dispositivo
- Verifica que ambos están en la misma red WiFi
- Usa `ipconfig` para obtener tu IP (busca "IPv4 Address")
- Intenta: `http://<tu-IP>:8000/dashboard`
- Si no funciona, el firewall de Windows puede estar bloqueando:
  - Abre: Windows Defender Firewall → Allow an app → Python

### El dashboard no muestra datos
- Verifica que la API está respondiendo: `curl http://localhost:8000/status`
- Revisa la consola de api_agencia.py para errores

## Archivos Relacionados

- `api_agencia.py` - Servidor API (ahora sirve también el dashboard)
- `dashboard_standalone.html` - Dashboard (ahora integrado)
- `arrancar_simple.bat` - Script para iniciar (ya no necesita dashboard_web.py)
- `limpiar_sistema.bat` - Si hay conflictos de puertos

## Nota Importante

El archivo `dashboard_web.py` ya **no es necesario**. El nuevo sistema:
- Usa un solo proceso Python (`api_agencia.py`)
- Elimina conflictos de puerto (antes: 8000 API + 8080 Dashboard)
- Es más rápido y confiable
- Funciona desde cualquier dispositivo

---

**Status**: ✅ Completado y listo para usar
**Fecha**: 2026-03-02
**Tested**: API sirve HTML correctamente
