"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: API REST de la Agencia Santi v1.0. Expone todos los agentes
             como endpoints HTTP. Permite conectar WhatsApp, dashboard web,
             apps externas y sistema de clientes. Corre en localhost:8000.
TECNOLOGÍA: http.server (stdlib), json, subprocess
"""



import os
import sys
import json
import time
import subprocess
import threading
import io as _io
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# ---------------------------------------------
#  CONFIGURACION
# ---------------------------------------------

BASE_DIR     = os.path.dirname(os.path.abspath(__file__))
HABILIDADES  = os.path.join(BASE_DIR, "habilidades.json")
LOG_API      = os.path.join(BASE_DIR, "registro_noche.txt")
PUERTO       = 8000
API_KEY      = "santi-agencia-2026"   # Cambiar en produccion
TIMEOUT_AGENTE = 30
MAX_HISTORIAL  = 100

# Cache de resultados (evita recalcular lo mismo)
cache = {}
cache_lock = threading.Lock()
historial_requests = []

# ---------------------------------------------
#  UTILIDADES
# ---------------------------------------------

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = f"[{ts}] [API] {msg}"
    print(linea)
    try:
        with open(LOG_API, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

def cargar_habilidades():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def ejecutar_agente(archivo, params="", timeout=TIMEOUT_AGENTE):
    ruta = os.path.join(BASE_DIR, archivo)
    if not os.path.exists(ruta):
        return False, f"Agente {archivo} no encontrado"
    cmd = [sys.executable, ruta]
    if params:
        cmd.extend(str(p) for p in params.split() if p)
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=timeout, cwd=BASE_DIR
        )
        salida = (r.stdout or "").strip()
        if not salida and r.stderr:
            return False, r.stderr[:300]
        return True, salida or "Sin output"
    except subprocess.TimeoutExpired:
        return False, f"Timeout ({timeout}s)"
    except Exception as e:
        return False, str(e)

def respuesta_json(handler, status, data):
    body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", len(body))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
    handler.end_headers()
    handler.wfile.write(body)

def verificar_auth(handler):
    auth = handler.headers.get("Authorization", "")
    if not auth:
        # Tambien aceptar via query param ?key=
        parsed = urlparse(handler.path)
        params = parse_qs(parsed.query)
        key = params.get("key", [""])[0]
        return key == API_KEY
    return auth.replace("Bearer ", "").strip() == API_KEY

def registrar_request(metodo, ruta, status, duracion_ms):
    historial_requests.append({
        "ts": datetime.now().strftime('%H:%M:%S'),
        "metodo": metodo,
        "ruta": ruta,
        "status": status,
        "ms": duracion_ms
    })
    if len(historial_requests) > MAX_HISTORIAL:
        historial_requests.pop(0)

# ---------------------------------------------
#  HANDLER PRINCIPAL
# ---------------------------------------------

class AgenciaHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # Silenciar log por defecto del servidor

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization, Content-Type")
        self.end_headers()

    def do_GET(self):
        inicio = time.time()
        parsed = urlparse(self.path)
        ruta   = parsed.path.rstrip("/")
        params = parse_qs(parsed.query)

        # -- Rutas publicas (sin auth) --------------
        if ruta == "" or ruta == "/":
            data = {
                "nombre": "Agencia Santi API",
                "version": "1.0",
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "endpoints": [
                    "GET  /agentes          — lista todos los agentes",
                    "GET  /agentes/{nombre} — info de un agente",
                    "GET  /areas            — agentes agrupados por area",
                    "GET  /status           — estado del sistema",
                    "GET  /historial        — ultimas requests",
                    "POST /ejecutar         — ejecutar un agente",
                    "POST /consulta         — lenguaje natural al Clawbot",
                ]
            }
            respuesta_json(self, 200, data)
            registrar_request("GET", ruta, 200, int((time.time()-inicio)*1000))
            return

        if ruta == "/ping":
            respuesta_json(self, 200, {"pong": True, "ts": datetime.now().isoformat()})
            return

        # -- Rutas con auth -------------------------
        if not verificar_auth(self):
            respuesta_json(self, 401, {"error": "No autorizado. Usa header Authorization: Bearer santi-agencia-2026"})
            registrar_request("GET", ruta, 401, int((time.time()-inicio)*1000))
            return

        habilidades = cargar_habilidades()

        # GET /agentes
        if ruta == "/agentes":
            agentes = []
            for archivo, info in habilidades.items():
                agentes.append({
                    "archivo": archivo,
                    "descripcion": info.get("descripcion", ""),
                    "area": info.get("categoria", ""),
                    "salud": info.get("salud", "OK"),
                    "ordenes": info.get("ordenes", [])
                })
            respuesta_json(self, 200, {
                "total": len(agentes),
                "agentes": agentes
            })

        # GET /agentes/{nombre}
        elif ruta.startswith("/agentes/"):
            nombre = ruta.split("/agentes/")[1]
            if nombre in habilidades:
                info = habilidades[nombre]
                # Leer primeras lineas del codigo
                preview = ""
                ruta_py = os.path.join(BASE_DIR, nombre)
                if os.path.exists(ruta_py):
                    with open(ruta_py, "r", encoding="utf-8", errors="replace") as f:
                        preview = "".join(f.readlines()[:15])
                respuesta_json(self, 200, {
                    "archivo": nombre,
                    "info": info,
                    "preview_codigo": preview
                })
            else:
                respuesta_json(self, 404, {"error": f"Agente '{nombre}' no encontrado"})

        # GET /areas
        elif ruta == "/areas":
            areas = {}
            for archivo, info in habilidades.items():
                area = info.get("categoria", "GENERAL")
                if area not in areas:
                    areas[area] = []
                areas[area].append(archivo)
            respuesta_json(self, 200, {
                "total_areas": len(areas),
                "total_agentes": len(habilidades),
                "areas": {k: {"cantidad": len(v), "agentes": v} for k, v in sorted(areas.items())}
            })

        # GET /status
        elif ruta == "/status":
            total = len(habilidades)
            ok    = sum(1 for v in habilidades.values() if v.get("salud") == "OK")
            log_size = 0
            if os.path.exists(LOG_API):
                log_size = round(os.path.getsize(LOG_API) / (1024*1024), 2)

            # Leer ultimas lineas del log
            ultimas_lineas = []
            try:
                with open(LOG_API, "r", encoding="utf-8", errors="replace") as f:
                    ultimas_lineas = [l.strip() for l in f.readlines()[-10:] if l.strip()]
            except Exception:
                pass

            respuesta_json(self, 200, {
                "status": "online",
                "timestamp": datetime.now().isoformat(),
                "agentes": {"total": total, "saludables": ok},
                "log_size_mb": log_size,
                "ultimas_actividades": ultimas_lineas,
                "requests_recientes": len(historial_requests)
            })

        # GET /historial
        elif ruta == "/historial":
            respuesta_json(self, 200, {
                "total": len(historial_requests),
                "requests": list(reversed(historial_requests[-20:]))
            })

        else:
            respuesta_json(self, 404, {"error": f"Ruta '{ruta}' no encontrada"})

        registrar_request("GET", ruta, 200, int((time.time()-inicio)*1000))

    def do_POST(self):
        inicio = time.time()
        parsed = urlparse(self.path)
        ruta   = parsed.path.rstrip("/")

        if not verificar_auth(self):
            respuesta_json(self, 401, {"error": "No autorizado"})
            return

        # Leer body
        body = {}
        try:
            length = int(self.headers.get("Content-Length", 0))
            if length > 0:
                raw = self.rfile.read(length)
                body = json.loads(raw.decode("utf-8"))
        except Exception as e:
            respuesta_json(self, 400, {"error": f"Body JSON invalido: {e}"})
            return

        # POST /ejecutar
        # Body: {"agente": "calculadora_roi.py", "params": "2000000 14000 2800 20000"}
        if ruta == "/ejecutar":
            agente = body.get("agente", "")
            params = body.get("params", "")
            usar_cache = body.get("cache", True)

            if not agente:
                respuesta_json(self, 400, {"error": "Falta campo 'agente'"})
                return

            habilidades = cargar_habilidades()
            if agente not in habilidades:
                respuesta_json(self, 404, {"error": f"Agente '{agente}' no registrado"})
                return

            # Revisar cache
            cache_key = f"{agente}:{params}"
            if usar_cache:
                with cache_lock:
                    if cache_key in cache:
                        cached = cache[cache_key]
                        if time.time() - cached["ts"] < 300:  # 5 min cache
                            respuesta_json(self, 200, {**cached["data"], "cache": True})
                            return

            log(f"Ejecutando {agente} params='{params}'")
            exito, output = ejecutar_agente(agente, params)

            data = {
                "agente": agente,
                "params": params,
                "exito": exito,
                "output": output,
                "timestamp": datetime.now().isoformat(),
                "cache": False
            }

            if exito and usar_cache:
                with cache_lock:
                    cache[cache_key] = {"ts": time.time(), "data": data}

            respuesta_json(self, 200 if exito else 500, data)
            registrar_request("POST", ruta, 200 if exito else 500, int((time.time()-inicio)*1000))

        # POST /ejecutar/batch
        # Body: {"tareas": [{"agente": "x.py", "params": "..."}, ...]}
        elif ruta == "/ejecutar/batch":
            tareas = body.get("tareas", [])
            if not tareas:
                respuesta_json(self, 400, {"error": "Falta campo 'tareas'"})
                return
            if len(tareas) > 10:
                respuesta_json(self, 400, {"error": "Maximo 10 tareas por batch"})
                return

            resultados = []
            for tarea in tareas:
                agente = tarea.get("agente", "")
                params = tarea.get("params", "")
                exito, output = ejecutar_agente(agente, params)
                resultados.append({
                    "agente": agente,
                    "exito": exito,
                    "output": output
                })
                time.sleep(0.5)

            respuesta_json(self, 200, {
                "batch": len(resultados),
                "resultados": resultados,
                "timestamp": datetime.now().isoformat()
            })

        # POST /consulta
        # Body: {"mensaje": "analiza depa de 2M en Polanco"}
        elif ruta == "/consulta":
            mensaje = body.get("mensaje", "").strip()
            if not mensaje:
                respuesta_json(self, 400, {"error": "Falta campo 'mensaje'"})
                return

            log(f"Consulta Clawbot: {mensaje[:60]}")
            exito, output = ejecutar_agente(
                "orquestador_clawbot.py",
                mensaje.replace('"', '').replace("'", ""),
                timeout=60
            )

            respuesta_json(self, 200, {
                "consulta": mensaje,
                "respuesta": output,
                "exito": exito,
                "timestamp": datetime.now().isoformat()
            })

        # POST /cache/limpiar
        elif ruta == "/cache/limpiar":
            with cache_lock:
                n = len(cache)
                cache.clear()
            respuesta_json(self, 200, {"limpiado": n, "mensaje": f"{n} entradas eliminadas del cache"})

        else:
            respuesta_json(self, 404, {"error": f"Ruta POST '{ruta}' no encontrada"})

        registrar_request("POST", ruta, 200, int((time.time()-inicio)*1000))


# ---------------------------------------------
#  SERVIDOR
# ---------------------------------------------

def iniciar_servidor():
    log("=" * 55)
    log("AGENCIA SANTI — API REST v1.0")
    log(f"Puerto: {PUERTO}")
    log(f"URL:    http://localhost:{PUERTO}")
    log(f"Auth:   Bearer {API_KEY}")
    log("=" * 55)
    log("Endpoints disponibles:")
    log("  GET  /              — info de la API")
    log("  GET  /agentes       — lista todos los agentes")
    log("  GET  /areas         — agentes por area")
    log("  GET  /status        — estado del sistema")
    log("  POST /ejecutar      — ejecutar un agente")
    log("  POST /ejecutar/batch— ejecutar varios agentes")
    log("  POST /consulta      — consulta en lenguaje natural")
    log("=" * 55)

    servidor = HTTPServer(("0.0.0.0", PUERTO), AgenciaHandler)
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        log("API detenida.")
        servidor.server_close()

if __name__ == "__main__":
    iniciar_servidor()