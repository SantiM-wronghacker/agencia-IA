"""
AREA: CEREBRO
DESCRIPCION: Orquestador de Way2Theunknown, v1.0 — Clawbot-style
             Memoria de sesion, params con regex, deteccion de seguimiento.
TECNOLOGIA: llm_router, subprocess, re
"""

import os
import sys
import re
import json
import time
import subprocess
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB
except ImportError:
    WEB = False

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

try:
    from llm_router import completar_simple as ia
except ImportError:
    from groq import Groq
    _g = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    def ia(prompt, **kw):
        r = _g.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=2000
        )
        return r.choices[0].message.content.strip()

BASE    = os.path.dirname(os.path.abspath(__file__))
NOMBRE  = "Way2Theunknown"
MODELO  = "agencia de viajes, dominio way2theunknown.com, fee 8%, mercado mexicano"
AGENTES = [
    "agentes/cotizador_viaje.py",
    "agentes/buscador_plusvalia.py",
    "agentes/calculadora_fee_viaje.py",
    "agentes/generador_itinerario_viaje.py",
    "agentes/web_builder.py",
]

MAX_AGENTES    = 4
TIMEOUT_AGENTE = 60

# Palabras clave para detectar solicitudes de sitio web
PALABRAS_WEB = [
    "sitio web", "pagina web", "página web", "website", "html", "css",
    "landing", "index", "home", "web", "página", "pagina", "diseño",
    "generar sitio", "crear sitio", "construir sitio", "hacer sitio",
    "generar pagina", "crear pagina", "destinos.html", "servicios.html",
]

# Palabras clave de acciones externas que requieren credenciales
PALABRAS_EXTERNAS = [
    "publicar", "postear", "responder mensaje", "responder comentario",
    "subir a", "deploy", "desplegar", "facebook", "instagram", "twitter",
    "tiktok", "whatsapp", "telegram", "email", "correo", "enviar",
    "wordpress", "editar pagina", "modificar sitio", "actualizar sitio",
    "shopify", "mercadolibre", "stripe", "pago", "campana", "anuncio",
    "newsletter", "mailchimp", "google ads", "meta ads",
]

# Importar sistema de credenciales
PROYECTO_ID = "way2theunknown"
try:
    sys.path.insert(0, str(Path(BASE).parent))
    from gestor_credenciales import credenciales_faltantes as _cred_faltantes
    from conector_plataformas import verificar_y_ejecutar as _verificar_creds
    from detector_plataforma import detectar_hosting as _detectar_hosting
    CREDS_DISPONIBLE = True
except ImportError:
    CREDS_DISPONIBLE = False

def log(msg):
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"[{ts}] [{NOMBRE[:14]}] {msg}", flush=True)

# ============================================
# EXTRACCION DE PARAMETROS — DOMINIO ESPECIFICO
# ============================================
def extraer_parametros(consulta, params_previos=None):
    """Extrae parametros numericos del dominio de Way2Theunknown,."""
    consulta_lower = consulta.lower()
    params = dict(params_previos) if params_previos else {}

    # MONTO
    m = re.search('\\$?\\s*(\\d+(?:[,\\.]\\d+)*)', consulta_lower)
    if m:
        params['monto'] = float(m.group(1).replace(',', ''))

    # CANTIDAD
    m = re.search('(\\d+)\\s*(?:unidades?|piezas?)', consulta_lower)
    if m:
        params['cantidad'] = int(m.group(1).replace(',', '').replace('.', ''))

    # PERSONAS
    m = re.search('(\\d+)\\s*personas?', consulta_lower)
    if m:
        params['personas'] = int(m.group(1).replace(',', '').replace('.', ''))

    # Defaults del dominio
    params.setdefault('monto', 1000.0)
    params.setdefault('cantidad', 1)
    params.setdefault('personas', 1)

    log('Params: ' + str(params))
    return params

# ============================================
# DETECCION DE SEGUIMIENTO
# ============================================
def es_seguimiento(consulta, historial):
    if not historial:
        return False
    indicadores = [
        "y si", "que pasa si", "que pasaria si", "y con", "ahora con",
        "cambia", "baja", "sube", "reduce", "aumenta", "y para",
        "en cambio", "en vez", "en lugar", "y si fuera", "mejor con"
    ]
    return any(ind in consulta.lower() for ind in indicadores)

# ============================================
# EXTRACCION INTELIGENTE DE NUMEROS
# ============================================
def extraer_numeros_clave(output_raw):
    if not output_raw:
        return "[Sin output]"
    lineas = output_raw.split("\n")
    nums, resumen = [], []
    for ln in lineas:
        s = ln.strip()
        if not s: continue
        if re.search(r'\$[\d,]+|\d+[\.,]\d+%?|\d{4,}', s):
            nums.append(s)
        elif any(kw in s.lower() for kw in [
            "total", "pago", "mensual", "roi", "flujo", "costo",
            "recomend", "resultado", "ganancia", "precio", "subtotal"
        ]):
            resumen.append(s)
    resultado = resumen[:5] + nums[:10]
    return "\n".join(resultado) if resultado else "\n".join(lineas[:15])

# ============================================
# ORQUESTADOR PRINCIPAL
# ============================================
class OrquestadorProyecto:

    def __init__(self):
        self.memoria_equipo = []
        self.historial      = []
        self.params_previos = None
        self.sesion_id      = str(int(time.time()))[-6:]

    def director_seleccionar(self, consulta, params, contexto_previo=""):
        agentes_txt = "\n".join([f"- {a}" for a in AGENTES])
        params_txt  = " | ".join([f"{k}={v}" for k, v in params.items()])
        ctx_txt     = f"\nCONTEXTO PREVIO:\n{contexto_previo}" if contexto_previo else ""
        prompt = (
            f"Eres director de {NOMBRE}.\n"
            f"Negocio: {MODELO}\n"
            f"Consulta del cliente: {consulta}\n"
            f"Parametros extraidos: {params_txt}\n"
            f"{ctx_txt}\n"
            f"Agentes disponibles:\n{agentes_txt}\n\n"
            f"Selecciona max {MAX_AGENTES} agentes mas utiles. "
            "Para cada uno define los argumentos concretos de sys.argv.\n"
            'RESPONDE SOLO este JSON:\n'
            '{"analisis":"que pide el usuario en 1 frase","subtareas":['
            '{"paso":1,"agente":"agentes/archivo.py","objetivo":"que logra","parametros":"args exactos"}'
            ']}' 
        )
        respuesta = ia(prompt)
        if not respuesta:
            return None
        if "```" in respuesta:
            for parte in respuesta.split("```"):
                if "{" in parte:
                    respuesta = parte.strip().lstrip("json").strip()
                    break
        try:
            return json.loads(respuesta.strip())
        except Exception as e:
            log(f"Error parseando plan: {e}")
            return None

    def ejecutar_agente(self, archivo, parametros=""):
        ruta = os.path.join(BASE, archivo)
        if not os.path.exists(ruta):
            log(f"[WARN] No existe: {ruta}")
            return False, f"[ERROR] {archivo} no existe"
        cmd = [sys.executable, ruta]
        if parametros and parametros.strip():
            cmd.extend(parametros.split())
        try:
            r = subprocess.run(
                cmd, capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=TIMEOUT_AGENTE, cwd=BASE
            )
            salida = r.stdout.strip()
            if not salida and r.stderr:
                return False, f"[ERROR] {r.stderr[:200]}"
            return True, salida or "[Sin output]"
        except subprocess.TimeoutExpired:
            return False, f"[TIMEOUT] {archivo} > {TIMEOUT_AGENTE}s"
        except Exception as e:
            return False, f"[ERROR] {e}"

    def interpretar_aporte(self, subtarea, output_raw):
        memoria_txt = ""
        for m in self.memoria_equipo:
            memoria_txt += f'\n[{m["agente"]}]: {m["aporte"][:200]}'
        output_limpio = extraer_numeros_clave(output_raw)
        prompt = (
            f"Agente especialista en {NOMBRE}.\n"
            f"Rol: {subtarea['objetivo']}\n"
            f"Equipo sabe:{memoria_txt if memoria_txt else ' (eres el primero)'}\n\n"
            f"Datos:\n{output_limpio}\n\n"
            "Extrae 3-5 datos clave con numeros exactos. Max 100 palabras. Sin markdown."
        )
        return ia(prompt) or output_limpio[:300]

    def director_sintetizar(self, consulta, params, contexto_previo=""):
        aportes_txt = ""
        for m in self.memoria_equipo:
            aportes_txt += f'\n\n[{m["agente"]}]\n{m["aporte"]}'
        params_txt = " | ".join([f"{k}={v}" for k, v in params.items()])
        ctx_txt    = f"\nCONTEXTO PREVIO:\n{contexto_previo}" if contexto_previo else ""
        prompt = (
            f"Director de {NOMBRE} ({MODELO}).\n"
            f"CONSULTA: {consulta}\n"
            f"PARAMETROS: {params_txt}\n"
            f"{ctx_txt}\n"
            f"APORTES:{aportes_txt}\n\n"
            "Responde directamente al cliente:\n"
            "1. Resumen con 3 datos clave\n"
            "2. Analisis: conviene? por que?\n"
            "3. Recomendacion concreta en 1-2 lineas\n"
            "Max 250 palabras. Sin frases genericas. Sin nombres de archivos."
        )
        fallback = "\n".join([f"• {m['agente']}: {m['aporte']}" for m in self.memoria_equipo])
        return ia(prompt) or fallback

    def construir_contexto(self):
        if not self.historial:
            return ""
        ctx = []
        for h in self.historial[-3:]:
            ctx.append(f"Consulta: {h['consulta']}\nResultado: {h['resumen'][:200]}")
        return "\n\n".join(ctx)

    def respuesta_directa(self, consulta, contexto=""):
        ctx_txt = f"\nContexto previo:\n{contexto}" if contexto else ""
        prompt = f"Eres experto en {NOMBRE} ({MODELO}).{ctx_txt}\nConsulta: {consulta}\nDatos concretos. Max 200 palabras."
        return ia(prompt) or "No pude procesar la consulta."

    def requiere_credenciales(self, consulta):
        """Detecta si la tarea requiere acceso a plataformas externas."""
        c = consulta.lower()
        return any(p in c for p in PALABRAS_EXTERNAS)

    def verificar_credenciales(self, consulta):
        """
        Verifica si hay credenciales necesarias para la tarea.
        Retorna (puede_proceder, mensaje_al_cliente).
        """
        if not CREDS_DISPONIBLE:
            return True, ""  # Sin modulo de creds, proceder normalmente

        faltantes = _cred_faltantes(PROYECTO_ID, consulta)
        if not faltantes:
            return True, ""

        # Construir mensaje claro para el cliente
        lineas = [
            f"Para ejecutar esta tarea necesito acceso a {len(faltantes)} plataforma(s).",
            "Por favor configura las siguientes credenciales:\n"
        ]
        for f in faltantes:
            lineas.append(f"  [{f['nombre']}]")
            lineas.append(f"    Campos: {', '.join(f['campos_requeridos'])}")
            lineas.append(f"    Como obtenerlas: {f['instrucciones']}")
            lineas.append("")

        lineas.append("Puedes configurarlas desde el Dashboard > Admin > Credenciales")
        lineas.append(f"o ejecutar: python gestor_credenciales.py --guardar {PROYECTO_ID} <plataforma>")

        return False, "\n".join(lineas)

    def es_solicitud_web(self, consulta):
        """Detecta si la consulta pide generar/modificar el sitio web."""
        c = consulta.lower()
        return any(p in c for p in PALABRAS_WEB)

    def manejar_sitio_web(self, consulta):
        """Ejecuta web_builder.py y retorna resultado."""
        log("Detectada solicitud de sitio web — ejecutando web_builder")
        print(f"\n   [WEB] Generando sitio web de {NOMBRE}...")

        web_builder = os.path.join(BASE, "agentes", "web_builder.py")
        if not os.path.exists(web_builder):
            return f"Error: no se encontró agentes/web_builder.py"

        try:
            r = subprocess.run(
                [sys.executable, web_builder, consulta],
                capture_output=True, text=True,
                encoding="utf-8", errors="replace",
                timeout=60, cwd=BASE
            )
            salida = (r.stdout or "").strip()
            error  = (r.stderr or "").strip()

            if r.returncode == 0 and salida:
                # Registrar en historial
                sitio_dir = os.path.join(BASE, "sitio_web")
                index_url = os.path.join(sitio_dir, "index.html")
                log(f"Sitio web generado correctamente")
                return (
                    f"✅ Sitio web de {NOMBRE} generado exitosamente.\n\n"
                    f"{salida}\n\n"
                    f"Abre en tu navegador:\n"
                    f"  file:///{index_url.replace(chr(92), '/')}"
                )
            else:
                return f"Error al generar sitio web:\n{error or salida or 'Sin detalle'}"
        except subprocess.TimeoutExpired:
            return "Timeout: El generador tardó más de 60 segundos."
        except Exception as e:
            return f"Error ejecutando web_builder: {e}"

    def procesar(self, consulta):
        print(f"\n{'-'*55}")
        print(f"[{NOMBRE}] {consulta[:70]}...")
        log(f"Consulta: {consulta[:100]}")

        # ── PASO 0: Verificar credenciales si la tarea requiere acceso externo ──
        if self.requiere_credenciales(consulta):
            puede, mensaje = self.verificar_credenciales(consulta)
            if not puede:
                log("Credenciales faltantes — informando al cliente")
                self.historial.append({
                    "consulta": consulta,
                    "resumen": "Credenciales faltantes",
                    "params": {},
                    "equipo": "verificacion_credenciales"
                })
                return mensaje

        # ── Detección especial: solicitud de sitio web ──────────────
        if self.es_solicitud_web(consulta):
            resultado = self.manejar_sitio_web(consulta)
            self.historial.append({
                "consulta": consulta,
                "resumen": resultado[:300],
                "params": {},
                "equipo": "agentes/web_builder.py"
            })
            return resultado

        seguimiento = es_seguimiento(consulta, self.historial)
        contexto    = self.construir_contexto()

        if seguimiento and self.params_previos:
            log("Seguimiento detectado — heredando params previos")
            params = extraer_parametros(consulta, self.params_previos)
        else:
            params = extraer_parametros(consulta)
        self.params_previos = params

        plan = self.director_seleccionar(consulta, params, contexto if seguimiento else "")
        if not plan:
            resultado = self.respuesta_directa(consulta, contexto)
            self.historial.append({"consulta": consulta, "resumen": resultado[:200], "params": params})
            return resultado

        subtareas = plan.get("subtareas", [])
        analisis  = plan.get("analisis", "")

        if not subtareas:
            resultado = self.respuesta_directa(consulta, contexto)
            self.historial.append({"consulta": consulta, "resumen": resultado[:200], "params": params})
            return resultado

        equipo_str = " -> ".join([s["agente"] for s in subtareas])
        print(f"   Equipo: {equipo_str}")
        print(f"   {analisis}")
        if seguimiento:
            print("   (Continuando conversacion previa)")

        self.memoria_equipo = []
        agentes_fallidos    = []

        for subtarea in subtareas:
            paso       = subtarea["paso"]
            agente     = subtarea["agente"]
            params_str = subtarea.get("parametros", "")
            print(f"\n   [{paso}/{len(subtareas)}] {agente}")
            if params_str:
                print(f"   Args: {params_str}")

            exito, output_raw = self.ejecutar_agente(agente, params_str)
            if not exito:
                log(f"[WARN] {agente} fallo: {output_raw[:80]}")
                agentes_fallidos.append(agente)
                continue

            aporte = self.interpretar_aporte(subtarea, output_raw)
            self.memoria_equipo.append({"paso": paso, "agente": agente, "aporte": aporte})
            print(f"   [OK] {aporte[:100]}...")
            time.sleep(0.5)

        if agentes_fallidos:
            log(f"Fallaron: {', '.join(agentes_fallidos)}")

        if not self.memoria_equipo:
            resultado = self.respuesta_directa(consulta, contexto)
        else:
            print("\n   Sintetizando...")
            resultado = self.director_sintetizar(consulta, params, contexto if seguimiento else "")

        self.historial.append({
            "consulta": consulta,
            "resumen":  (resultado or "")[:300],
            "params":   params,
            "equipo":   equipo_str
        })
        log(f"Completado. Equipo: {equipo_str}")
        return resultado

    def mostrar_historial(self):
        if not self.historial:
            print("Sin historial en esta sesion.")
            return
        print(f"\n{'-'*55}")
        print(f"HISTORIAL ({len(self.historial)} consultas):")
        for i, h in enumerate(self.historial, 1):
            params_txt = " | ".join([f"{k}={v}" for k, v in h["params"].items()])
            print(f"\n[{i}] {h['consulta'][:60]}")
            print(f"    Equipo: {h.get('equipo', 'directo')}")
            print(f"    Params: {params_txt}")

# ============================================
# PUNTO DE ENTRADA
# ============================================
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] not in ("--interactive", "-i"):
        orq = OrquestadorProyecto()
        print("\n" + "="*55)
        print(NOMBRE + " — Sistema de IA")
        print("="*55)
        resultado = orq.procesar(" ".join(sys.argv[1:]))
        print("\n" + resultado)
        print("="*55)
    else:
        orq = OrquestadorProyecto()
        print("+" + "="*53 + "+")
        print(f"|  {NOMBRE:<51}  |")
        print(f"|  {MODELO[:51]:<51}  |")
        print("+" + "="*53 + "+")
        print("|  'historial' -> ver consultas previas         |")
        print("|  'equipo'    -> ver ultimo equipo             |")
        print("|  'salir'     -> terminar                      |")
        print("+" + "="*53 + "+\n")
        while True:
            try:
                consulta = input("Consulta: ").strip()
                if not consulta: continue
                if consulta.lower() in ("salir", "exit", "quit"): break
                if consulta.lower() == "equipo":
                    for m in orq.memoria_equipo:
                        print(f"  [{m['paso']}] {m['agente']} -> {m['aporte'][:100]}")
                    continue
                if consulta.lower() == "historial":
                    orq.mostrar_historial()
                    continue
                resultado = orq.procesar(consulta)
                print(f"\n{'='*55}")
                print(resultado)
                print(f"{'='*55}\n")
            except KeyboardInterrupt:
                print(f"\n[{NOMBRE}] Apagado.")
                break