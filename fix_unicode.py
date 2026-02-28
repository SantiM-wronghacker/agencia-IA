"""
Arregla UnicodeEncodeError en todos los archivos Python de la agencia.
Reemplaza emojis y caracteres especiales por texto ASCII simple.
"""
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

ARCHIVOS = [
    "fabrica_agentes.py",
    "noche_total.py",
    "auto_run.py",
    "sistema_maestro.py",
    "api_agencia.py",
    "dashboard_web.py",
    "orquestador_clawbot.py",
]

REEMPLAZOS = [
    ("[FABRICA]", "[FABRICA]"), ("[OK]", "[OK]"), ("[ERROR]", "[ERROR]"),
    ("[WARN]", "[WARN]"), ("[WARN]",  "[WARN]"), ("[INFO]", "[INFO]"), ("[INFO]",  "[INFO]"),
    ("[NOCHE]", "[NOCHE]"), ("[RUN]", "[RUN]"), ("[FIX]", "[FIX]"), ("[STOP]", "[STOP]"),
    ("[STATS]", "[STATS]"), ("[LISTA]", "[LISTA]"), ("[DOC]", "[DOC]"), ("[CEREBRO]", "[CEREBRO]"),
    ("[META]", "[META]"), ("[BUSCAR]", "[BUSCAR]"), ("[FAST]", "[FAST]"), ("[NOCHE]", "[NOCHE]"),
    ("[QA]","[QA]"), ("[QA]", "[QA]"), ("[PAUSA]", "[PAUSA]"), ("[ALERTA]", "[ALERTA]"),
    ("[OK]",  "[OK]"), ("[FAIL]",  "[FAIL]"), ("->",  "->"), ("<-",  "<-"),
    ("+", "+"), ("+", "+"), ("+", "+"), ("+", "+"),
    ("+", "+"), ("+", "+"), ("|", "|"), ("=", "="),
    ("-", "-"), ("|", "|"), ("+", "+"), ("+", "+"),
    ("+", "+"), ("+", "+"), ("+", "+"), ("+", "+"),
    ("=", "="), ("|", "|"), (">", ">"), ("<", "<"),
]

PARCHE_VIEJO = """"""

def limpiar(archivo):
    if not os.path.exists(archivo):
        print(f"  No encontrado: {archivo}")
        return

    with open(archivo, "r", encoding="utf-8", errors="replace") as f:
        texto = f.read()

    # Quitar parche viejo
    texto = texto.replace(PARCHE_VIEJO, "").strip()

    # Aplicar reemplazos
    for orig, remp in REEMPLAZOS:
        texto = texto.replace(orig, remp)

    # Forzar ASCII en cualquier caracter raro restante
    lineas_safe = []
    for linea in texto.split("\n"):
        try:
            linea.encode("cp1252")
            lineas_safe.append(linea)
        except (UnicodeEncodeError, UnicodeDecodeError):
            safe = linea.encode("cp1252", errors="replace").decode("cp1252")
            lineas_safe.append(safe)

    with open(archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_safe))

    print(f"  OK: {archivo}")

print("Limpiando archivos...")
for a in ARCHIVOS:
    limpiar(a)

# Buscar otros con TextIOWrapper mal puesto
print("\nBuscando otros archivos con parche roto...")
for f in os.listdir("."):
    if f.endswith(".py") and f not in ARCHIVOS:
        try:
            c = open(f, "r", encoding="utf-8", errors="replace").read()
            if "TextIOWrapper" in c:
                limpiar(f)
        except Exception:
            pass

print("\nListo. Corre .\\arrancar.bat")