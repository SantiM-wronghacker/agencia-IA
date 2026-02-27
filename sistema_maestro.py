"""
ÁREA: CEREBRO
DESCRIPCIÓN: Sistema Maestro v1.0 — Integrador total de la Agencia Santi.
             Arranca automáticamente al iniciar Windows. Gestiona en paralelo:
             fábrica de agentes, modo noche, monitor de salud, limpieza de logs,
             y consola central de control. Un solo proceso que hace funcionar todo.
TECNOLOGÍA: Python estándar, threading, subprocess
"""

import os
import sys
import json
import time
import threading
import subprocess
import shutil
import re
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURACIÓN
# ─────────────────────────────────────────────

BASE_DIR        = os.path.dirname(os.path.abspath(__file__))
LOG             = os.path.join(BASE_DIR, "registro_noche.txt")
HABILIDADES     = os.path.join(BASE_DIR, "habilidades.json")
BUS             = os.path.join(BASE_DIR, "bus_mensajes.json")
MISIONES        = os.path.join(BASE_DIR, "misiones.txt")
RUNS_DIR        = os.path.join(BASE_DIR, "runs")
PROYECTOS_QUEUE = os.path.join(BASE_DIR, "proyectos_queue")
PROYECTOS_DONE  = os.path.join(BASE_DIR, "proyectos_queue", "procesados")
MAX_LOG_MB      = 5       # Limpiar log si supera este tamaño
CICLO_MONITOR   = 60      # Segundos entre chequeos de salud
CICLO_LIMPIEZA  = 300     # Segundos entre limpiezas automáticas
CICLO_PROYECTOS = 30      # Segundos entre chequeos de proyectos_queue
TIMEOUT_PROCESO = 180     # Timeout para scripts cortos
TIMEOUT_NOCHE   = 3600    # 1 hora para noche_total
TIMEOUT_MISIONES = 1800   # 30 min para auto_run (200+ misiones)

os.makedirs(RUNS_DIR, exist_ok=True)
os.makedirs(PROYECTOS_QUEUE, exist_ok=True)
os.makedirs(PROYECTOS_DONE, exist_ok=True)

# ─────────────────────────────────────────────
#  ESTADO GLOBAL
# ─────────────────────────────────────────────

estado = {
    "inicio":           datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    "fabrica_activa":   False,
    "noche_activa":     False,
    "proyectos_activo": False,
    "lotes_generados":  0,
    "agentes_total":    0,
    "agentes_con_web":  0,
    "ciclos_noche":     0,
    "errores":          0,
    "ultimo_ciclo":     "—",
    "ultimo_agente":    "—",
    "log_size_mb":      0,
    "misiones_pendientes": 0,
    "proyectos_creados": 0,
    "ultimo_proyecto":  "—",
}

log_lock = threading.Lock()

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

def log(msg, nivel="INFO"):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    iconos = {"INFO": "ℹ", "OK": "✅", "WARN": "⚠", "ERROR": "❌", "MASTER": "🏭"}
    icono = iconos.get(nivel, "ℹ")
    linea = f"[{ts}] [{nivel}] {icono} [MAESTRO] {msg}"
    with log_lock:
        print(linea)
        try:
            with open(LOG, "a", encoding="utf-8") as f:
                f.write(linea + "\n")
        except Exception:
            pass

# ─────────────────────────────────────────────
#  EJECUTOR SEGURO DE SCRIPTS
# ─────────────────────────────────────────────

def ejecutar(script, args=None, timeout=TIMEOUT_PROCESO):
    ruta = os.path.join(BASE_DIR, script)
    if not os.path.exists(ruta):
        return False, f"{script} no encontrado"
    cmd = [sys.executable, ruta] + (args or [])
    try:
        r = subprocess.run(
            cmd, capture_output=True, text=True,
            encoding="utf-8", errors="replace",
            timeout=timeout, cwd=BASE_DIR
        )
        return r.returncode == 0, (r.stdout or r.stderr or "")[:300]
    except subprocess.TimeoutExpired:
        return False, f"Timeout {timeout}s"
    except Exception as e:
        return False, str(e)

# ─────────────────────────────────────────────
#  LECTOR DE HABILIDADES
# ─────────────────────────────────────────────

def contar_agentes():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            h = json.load(f)
        return len(h), sum(1 for v in h.values() if v.get("salud") == "OK")
    except Exception:
        return 0, 0

def contar_agentes_con_web():
    """Cuenta agentes que importan web_bridge (tienen acceso a internet)."""
    count = 0
    try:
        for f in os.listdir(BASE_DIR):
            if f.endswith(".py") and not f.startswith("__"):
                ruta = os.path.join(BASE_DIR, f)
                try:
                    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                        contenido = fh.read(2000)  # Solo primeros 2KB
                    if "import web_bridge" in contenido or "from web_bridge" in contenido:
                        count += 1
                except Exception:
                    pass
    except Exception:
        pass
    return count

def contar_misiones():
    try:
        with open(MISIONES, "r", encoding="utf-8", errors="replace") as f:
            lineas = [l for l in f.readlines() if l.strip()]
        return len(lineas)
    except Exception:
        return 0

# ─────────────────────────────────────────────
#  LIMPIADOR AUTOMÁTICO
# ─────────────────────────────────────────────

def limpiar_sistema():
    """Limpia logs pesados, backups viejos y archivos temporales."""
    log("Iniciando limpieza automática...")

    # Limpiar log si supera MAX_LOG_MB
    if os.path.exists(LOG):
        size_mb = os.path.getsize(LOG) / (1024 * 1024)
        estado["log_size_mb"] = round(size_mb, 2)
        if size_mb > MAX_LOG_MB:
            # Archivar últimas 500 líneas
            try:
                with open(LOG, "r", encoding="utf-8", errors="replace") as f:
                    lineas = f.readlines()
                ultimas = lineas[-500:]
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                archivo_hist = os.path.join(RUNS_DIR, f"log_historico_{ts}.txt")
                with open(archivo_hist, "w", encoding="utf-8") as f:
                    f.writelines(lineas[:-500])
                with open(LOG, "w", encoding="utf-8") as f:
                    f.writelines(ultimas)
                log(f"Log archivado ({size_mb:.1f}MB → 500 líneas activas)", "OK")
            except Exception as e:
                log(f"Error limpiando log: {e}", "WARN")

    # Mover .bak antiguos (más de 3 días) a runs/historico
    historico = os.path.join(RUNS_DIR, "historico")
    os.makedirs(historico, exist_ok=True)
    ahora = time.time()
    movidos = 0
    for f in os.listdir(BASE_DIR):
        es_bak = f.endswith(".bak") or ".bak.mejora_" in f or ".bak." in f
        if es_bak and not f.startswith("."):
            ruta = os.path.join(BASE_DIR, f)
            edad = (ahora - os.path.getmtime(ruta)) / 86400
            if edad > 3:
                try:
                    shutil.move(ruta, os.path.join(historico, f))
                    movidos += 1
                except Exception:
                    pass
    if movidos:
        log(f"{movidos} archivos .bak archivados", "OK")

    # Limpiar bus_mensajes.json si supera 500KB
    if os.path.exists(BUS):
        size_bus = os.path.getsize(BUS) / 1024
        if size_bus > 500:
            try:
                with open(BUS, "r", encoding="utf-8", errors="replace") as f:
                    bus_data = json.load(f)
                # Mantener solo últimos 50 mensajes
                if isinstance(bus_data, list) and len(bus_data) > 50:
                    bus_data = bus_data[-50:]
                    with open(BUS, "w", encoding="utf-8") as f:
                        json.dump(bus_data, f, indent=2, ensure_ascii=False)
                    log(f"Bus limpiado ({size_bus:.0f}KB → 50 mensajes)", "OK")
            except Exception:
                pass

    # Limpiar carpeta lote_nuevo si quedó con archivos
    lote_dir = os.path.join(BASE_DIR, "lote_nuevo")
    if os.path.exists(lote_dir):
        for f in os.listdir(lote_dir):
            try:
                os.remove(os.path.join(lote_dir, f))
            except Exception:
                pass

    log("Limpieza completada", "OK")


def hilo_limpieza():
    """Hilo que limpia el sistema cada CICLO_LIMPIEZA segundos."""
    while True:
        try:
            time.sleep(CICLO_LIMPIEZA)
            limpiar_sistema()
        except Exception as e:
            log(f"Error en limpieza: {e}", "WARN")

# ─────────────────────────────────────────────
#  MONITOR DE SALUD
# ─────────────────────────────────────────────

def hilo_monitor():
    """Monitorea el estado del sistema cada CICLO_MONITOR segundos."""
    while True:
        try:
            total, ok = contar_agentes()
            misiones = contar_misiones()
            estado["agentes_total"]      = total
            estado["misiones_pendientes"] = misiones
            estado["agentes_con_web"]    = contar_agentes_con_web()

            if os.path.exists(LOG):
                estado["log_size_mb"] = round(os.path.getsize(LOG) / (1024*1024), 2)

            # Alerta si hay agentes con problemas
            if total > 0 and ok < total * 0.8:
                log(f"Solo {ok}/{total} agentes saludables", "WARN")

            time.sleep(CICLO_MONITOR)
        except Exception as e:
            log(f"Error monitor: {e}", "WARN")
            time.sleep(CICLO_MONITOR)

# ─────────────────────────────────────────────
#  HILO: MODO NOCHE
# ─────────────────────────────────────────────

def hilo_noche():
    """
    Corre noche_total.py como subproceso persistente.
    noche_total ya tiene su propio bucle infinito interno.
    """
    estado["noche_activa"] = True
    log("Modo Noche activado como proceso persistente", "OK")
    while True:
        try:
            ruta = os.path.join(BASE_DIR, "noche_total.py")
            if not os.path.exists(ruta):
                log("noche_total.py no encontrado, esperando 60s...", "WARN")
                time.sleep(60)
                continue
            estado["ultimo_ciclo"] = datetime.now().strftime('%H:%M:%S')
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )
            for linea in proc.stdout:
                linea = linea.strip()
                if linea and any(k in linea for k in ["CICLO", "completado", "ERROR"]):
                    if "completado" in linea.lower():
                        estado["ciclos_noche"] += 1
                    with log_lock:
                        try:
                            with open(LOG, "a", encoding="utf-8") as f:
                                f.write("[NOCHE] " + linea + "\n")
                        except Exception:
                            pass
            proc.wait()
            log("noche_total.py terminó, reiniciando en 30s...", "WARN")
            time.sleep(30)
        except Exception as e:
            log(f"Error en noche: {e}", "ERROR")
            time.sleep(30)

# ─────────────────────────────────────────────
#  HILO: FÁBRICA DE AGENTES
# ─────────────────────────────────────────────

def hilo_fabrica():
    """Corre fabrica_agentes.py como subproceso continuo."""
    estado["fabrica_activa"] = True
    log("Fábrica de agentes activada", "OK")

    # La fábrica ya tiene su propio bucle infinito
    # La corremos como subproceso y la reiniciamos si muere
    while True:
        try:
            ruta = os.path.join(BASE_DIR, "fabrica_agentes.py")
            if not os.path.exists(ruta):
                log("fabrica_agentes.py no encontrado, esperando...", "WARN")
                time.sleep(60)
                continue

            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, encoding="utf-8", errors="replace"
            )

            # Leer output de la fábrica y reenviarlo al log
            for linea in proc.stdout:
                linea = linea.strip()
                if linea and ("FABRICA" in linea.upper() or "LOTE" in linea or "APROBADO" in linea):
                    if "APROBADO" in linea:
                        estado["lotes_generados"] += 1
                        match = re.search(r'(\w+\.py)', linea)
                        if match:
                            estado["ultimo_agente"] = match.group(1)
                    # Solo loggear líneas importantes para no saturar
                    if any(k in linea.upper() for k in ["LOTE", "APROBADO", "ERROR", "COMPLETADO", "FABRICA"]):
                        with log_lock:
                            try:
                                with open(LOG, "a", encoding="utf-8") as f:
                                    f.write(linea + "\n")
                            except Exception:
                                pass

            proc.wait()
            log("Fábrica terminó inesperadamente, reiniciando en 10s...", "WARN")
            time.sleep(10)

        except Exception as e:
            log(f"Error en fábrica: {e}", "ERROR")
            time.sleep(30)

# ─────────────────────────────────────────────
#  HILO: EJECUTOR DE MISIONES
# ─────────────────────────────────────────────

def hilo_misiones():
    """Ejecuta misiones pendientes. Timeout largo para cientos de misiones."""
    time.sleep(60)  # Esperar que arranquen los otros hilos primero
    while True:
        try:
            misiones = contar_misiones()
            if misiones > 0:
                log(f"Ejecutando {misiones} misiones (timeout 30min)...", "INFO")
                exito, output = ejecutar("auto_run.py", timeout=1800)
                if exito:
                    restantes = contar_misiones()
                    log(f"Misiones OK. Restantes: {restantes}", "OK")
                    estado["misiones_pendientes"] = restantes
                else:
                    log(f"Misiones: {output[:150]}", "WARN")
            time.sleep(600)  # 10 min entre intentos
        except Exception as e:
            log(f"Error misiones: {e}", "WARN")
            time.sleep(60)

# ─────────────────────────────────────────────
#  HILO: ORQUESTADOR DE PROYECTOS
# ─────────────────────────────────────────────

def hilo_proyectos():
    """
    Monitorea proyectos_queue/ cada 30s.
    Cuando encuentra un .txt, lo lee como descripcion de negocio,
    ejecuta orquestador_proyectos.py, y mueve el .txt a procesados/.
    """
    estado["proyectos_activo"] = True
    log("Orquestador de proyectos activado (monitorea proyectos_queue/)", "OK")

    while True:
        try:
            # Buscar archivos .txt en proyectos_queue/
            archivos_txt = []
            for f in os.listdir(PROYECTOS_QUEUE):
                if f.endswith(".txt") and os.path.isfile(os.path.join(PROYECTOS_QUEUE, f)):
                    archivos_txt.append(f)

            for archivo in archivos_txt:
                ruta = os.path.join(PROYECTOS_QUEUE, archivo)
                try:
                    with open(ruta, "r", encoding="utf-8", errors="replace") as fh:
                        descripcion = fh.read().strip()
                except Exception as e:
                    log(f"Error leyendo {archivo}: {e}", "WARN")
                    continue

                if not descripcion:
                    log(f"Archivo vacio: {archivo}, saltando", "WARN")
                    continue

                log(f"Nuevo proyecto detectado: {archivo}", "INFO")
                log(f"Descripcion: {descripcion[:100]}...", "INFO")

                # Ejecutar orquestador_proyectos.py con la descripcion
                exito, output = ejecutar(
                    "orquestador_proyectos.py",
                    args=[descripcion],
                    timeout=600  # 10 min max por proyecto
                )

                if exito:
                    estado["proyectos_creados"] += 1
                    estado["ultimo_proyecto"] = archivo.replace(".txt", "")
                    log(f"Proyecto '{archivo}' completado", "OK")
                else:
                    log(f"Proyecto '{archivo}' fallo: {output[:150]}", "ERROR")

                # Mover a procesados/ (exito o fallo)
                destino = os.path.join(PROYECTOS_DONE, archivo)
                try:
                    shutil.move(ruta, destino)
                except Exception as e:
                    log(f"Error moviendo {archivo}: {e}", "WARN")

            time.sleep(CICLO_PROYECTOS)

        except Exception as e:
            log(f"Error en hilo proyectos: {e}", "WARN")
            time.sleep(CICLO_PROYECTOS)

# ─────────────────────────────────────────────
#  CONSOLA CENTRAL
# ─────────────────────────────────────────────

def mostrar_dashboard():
    total, ok = contar_agentes()
    web_count = contar_agentes_con_web()
    estado["agentes_con_web"] = web_count
    print(f"""
╔══════════════════════════════════════════════════════════╗
║         AGENCIA SANTI — SISTEMA MAESTRO v1.1             ║
╠══════════════════════════════════════════════════════════╣
║  Inicio:        {estado['inicio']:<38}  ║
║  Agentes total: {total:<5}  Saludables: {ok:<5}  Con internet: {web_count:<4}║
║  Ciclos noche:  {estado['ciclos_noche']:<5}  Errores: {estado['errores']:<5}                    ║
║  Lotes fabrica: {estado['lotes_generados']:<5}  Ultimo: {estado['ultimo_agente']:<20}  ║
║  Misiones:      {estado['misiones_pendientes']:<5}  Log: {estado['log_size_mb']:<5}MB                      ║
║  Proyectos:     {estado['proyectos_creados']:<5}  Ultimo: {estado['ultimo_proyecto']:<20}  ║
║  Ultimo ciclo:  {estado['ultimo_ciclo']:<38}  ║
╠══════════════════════════════════════════════════════════╣
║  PROCESOS ACTIVOS:                                       ║
║  {'OK' if estado['fabrica_activa'] else '--'} Fabrica de agentes (bucle infinito)              ║
║  {'OK' if estado['noche_activa'] else '--'} Modo noche (ciclos cada 2 min)                  ║
║  {'OK' if estado['proyectos_activo'] else '--'} Orquestador proyectos (cada 30s)               ║
║  OK Monitor de salud (cada 60s)                          ║
║  OK Limpieza automatica (cada 5 min)                     ║
║  OK Ejecutor de misiones (cada 10 min)                   ║
║  OK API REST  — http://localhost:8000                    ║
║  OK Dashboard — http://localhost:8080                    ║
╠══════════════════════════════════════════════════════════╣
║  COMANDOS: 'status' 'agentes' 'limpiar' 'misiones' 'q'  ║
╚══════════════════════════════════════════════════════════╝""")

def consola_interactiva():
    """Consola central para controlar el sistema."""
    time.sleep(3)  # Esperar que arranquen los hilos
    mostrar_dashboard()

    while True:
        try:
            cmd = input("\n🏭 Maestro> ").strip().lower()

            if cmd in ("q", "quit", "exit", "salir"):
                log("Sistema maestro detenido manualmente.", "WARN")
                os._exit(0)

            elif cmd == "status":
                mostrar_dashboard()

            elif cmd == "agentes":
                total, ok = contar_agentes()
                try:
                    with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
                        h = json.load(f)
                    areas = {}
                    for v in h.values():
                        area = v.get("categoria", "GENERAL")
                        areas[area] = areas.get(area, 0) + 1
                    print(f"\n📊 AGENTES POR ÁREA ({total} total, {ok} OK):")
                    for area, count in sorted(areas.items(), key=lambda x: -x[1]):
                        print(f"   {area:<25} {count}")
                except Exception as e:
                    print(f"Error: {e}")

            elif cmd == "limpiar":
                limpiar_sistema()

            elif cmd == "misiones":
                misiones = contar_misiones()
                print(f"\n📋 {misiones} misiones pendientes en misiones.txt")
                if misiones > 0:
                    exito, _ = ejecutar("auto_run.py", timeout=300)
                    print("✅ Ejecutadas" if exito else "❌ Error al ejecutar")

            elif cmd == "log":
                if os.path.exists(LOG):
                    with open(LOG, "r", encoding="utf-8", errors="replace") as f:
                        lineas = f.readlines()
                    print(f"\n📄 Últimas 20 líneas del log:")
                    for l in lineas[-20:]:
                        print(l.rstrip())

            elif cmd == "help" or cmd == "?":
                print("""
Comandos disponibles:
  status    — Ver dashboard completo
  agentes   — Ver agentes por área
  limpiar   — Limpiar logs y backups ahora
  misiones  — Ver y ejecutar misiones pendientes
  log       — Ver últimas líneas del log
  q         — Detener el sistema""")

            elif cmd == "":
                continue

            else:
                print(f"Comando desconocido: '{cmd}'. Escribe 'help' para ver opciones.")

        except KeyboardInterrupt:
            log("Sistema maestro detenido con Ctrl+C.", "WARN")
            os._exit(0)
        except EOFError:
            # Sin consola interactiva (modo daemon)
            time.sleep(60)
        except Exception as e:
            log(f"Error en consola: {e}", "WARN")

# ─────────────────────────────────────────────
#  REGISTRO EN TAREA DE WINDOWS (arranque automático)
# ─────────────────────────────────────────────

def registrar_tarea_windows():
    """Registra el sistema para arrancar automáticamente con Windows."""
    try:
        python_exe = sys.executable
        script     = os.path.abspath(__file__)
        nombre     = "AgenciaSanti_SistemaMaestro"

        cmd_check = f'schtasks /query /tn "{nombre}" 2>nul'
        existe = os.system(cmd_check) == 0

        if not existe:
            cmd_crear = (
                f'schtasks /create /tn "{nombre}" '
                f'/tr "\\"{python_exe}\\" \\"{script}\\" --daemon" '
                f'/sc onlogon /rl highest /f'
            )
            resultado = os.system(cmd_crear)
            if resultado == 0:
                log(f"✅ Tarea '{nombre}' registrada — arrancará con Windows", "OK")
            else:
                log("⚠ No se pudo registrar tarea (ejecuta como administrador)", "WARN")
        else:
            log(f"Tarea '{nombre}' ya registrada en Windows", "INFO")

    except Exception as e:
        log(f"Error registrando tarea: {e}", "WARN")


# ─────────────────────────────────────────────
#  HILO: API REST
# ─────────────────────────────────────────────

def hilo_api():
    """Arranca la API REST en puerto 8000."""
    log('API REST activada en puerto 8000', 'OK')
    while True:
        try:
            ruta = os.path.join(BASE_DIR, 'api_agencia.py')
            if not os.path.exists(ruta):
                log('api_agencia.py no encontrado, esperando...', 'WARN')
                time.sleep(30)
                continue
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            proc.wait()
            log('API REST termino, reiniciando en 5s...', 'WARN')
            time.sleep(5)
        except Exception as e:
            log(f'Error en API: {e}', 'ERROR')
            time.sleep(15)

# ─────────────────────────────────────────────
#  HILO: DASHBOARD WEB
# ─────────────────────────────────────────────

def hilo_dashboard():
    """Arranca el dashboard web en puerto 8080."""
    log('Dashboard web activado en puerto 8080', 'OK')
    while True:
        try:
            ruta = os.path.join(BASE_DIR, 'dashboard_web.py')
            if not os.path.exists(ruta):
                log('dashboard_web.py no encontrado, esperando...', 'WARN')
                time.sleep(30)
                continue
            proc = subprocess.Popen(
                [sys.executable, ruta],
                cwd=BASE_DIR,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            proc.wait()
            log('Dashboard termino, reiniciando en 5s...', 'WARN')
            time.sleep(5)
        except Exception as e:
            log(f'Error en dashboard: {e}', 'ERROR')
            time.sleep(15)

# ─────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────

def main():
    modo_daemon = "--daemon" in sys.argv

    log("╔══════════════════════════════════════════════════════╗", "MASTER")
    log("║      AGENCIA SANTI — SISTEMA MAESTRO v1.0           ║", "MASTER")
    log("║      Iniciando todos los sistemas...                ║", "MASTER")
    log("╚══════════════════════════════════════════════════════╝", "MASTER")

    # Arranque automatico de Windows DESACTIVADO
    # Para reactivar: registrar_tarea_windows()

    # Limpieza inicial
    limpiar_sistema()

    # Arrancar todos los hilos en paralelo
    hilos = [
        threading.Thread(target=hilo_api,       daemon=True, name="API"),
        threading.Thread(target=hilo_dashboard, daemon=True, name="Dashboard"),
        threading.Thread(target=hilo_fabrica,   daemon=True, name="Fabrica"),
        threading.Thread(target=hilo_noche,     daemon=True, name="Noche"),
        threading.Thread(target=hilo_monitor,   daemon=True, name="Monitor"),
        threading.Thread(target=hilo_limpieza,  daemon=True, name="Limpieza"),
        threading.Thread(target=hilo_misiones,  daemon=True, name="Misiones"),
        threading.Thread(target=hilo_proyectos, daemon=True, name="Proyectos"),
    ]

    for hilo in hilos:
        hilo.start()
        log(f"Hilo '{hilo.name}' iniciado", "OK")
        time.sleep(1)

    log("Todos los sistemas activos. Agencia Santi operando.", "MASTER")

    # En modo daemon no hay consola interactiva
    if modo_daemon:
        log("Modo daemon — sin consola interactiva", "INFO")
        while True:
            time.sleep(300)
            total, ok = contar_agentes()
            log(f"Heartbeat — Agentes: {total} | Ciclos noche: {estado['ciclos_noche']} | Lotes fábrica: {estado['lotes_generados']}", "INFO")
    else:
        consola_interactiva()


if __name__ == "__main__":
    main()