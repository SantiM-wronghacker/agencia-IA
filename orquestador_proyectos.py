"""
AREA: CEREBRO
DESCRIPCION: Orquestador de Proyectos v3.0. Recibe descripcion de un negocio,
             busca agentes utiles en el catalogo por keywords (sin LLM extra),
             crea los que faltan con timeout de 60s un solo intento, y los que
             fallen van a misiones.txt para que la fabrica los complete despues.
TECNOLOGIA: llm_router, habilidades.json, ast, subprocess
"""

import os
import sys
import ast
import json
import time
import shutil
import subprocess
import re
import io as _io
from datetime import datetime

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

try:
    from llm_router import completar_simple as ia
except ImportError:
    from groq import Groq
    _g = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))
    def ia(prompt, **kw):
        r = _g.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3, max_tokens=3000
        )
        return r.choices[0].message.content.strip()

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
HABILIDADES = os.path.join(BASE_DIR, "habilidades.json")
MISIONES    = os.path.join(BASE_DIR, "misiones.txt")
LOG         = os.path.join(BASE_DIR, "registro_noche.txt")
PROYECTOS   = os.path.join(BASE_DIR, "proyectos")

# ─────────────────────────────────────────────
#  LOGGING
# ─────────────────────────────────────────────

def log(msg):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    linea = "[" + ts + "] [PROYECTOS] " + str(msg)
    try:
        print(linea, flush=True)
    except Exception:
        pass
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(linea + "\n")
    except Exception:
        pass

# ─────────────────────────────────────────────
#  JSON ROBUSTO — nunca falla por formato
# ─────────────────────────────────────────────

def extraer_json(texto, tipo="objeto"):
    """
    Extrae JSON de una respuesta del LLM aunque venga con markdown,
    texto extra, o formato sucio. tipo = 'objeto' o 'lista'
    """
    if not texto:
        return None

    # Limpiar markdown
    for bloque in texto.split("```"):
        limpio = bloque.strip().lstrip("json").strip()
        if tipo == "objeto" and limpio.startswith("{"):
            try:
                return json.loads(limpio)
            except Exception:
                pass
        if tipo == "lista" and limpio.startswith("["):
            try:
                return json.loads(limpio)
            except Exception:
                pass

    # Buscar directamente en el texto
    if tipo == "objeto":
        match = re.search(r'\{[\s\S]*\}', texto)
    else:
        match = re.search(r'\[[\s\S]*\]', texto)

    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass

    # Intentar reparar JSON comun: comillas simples, comas finales
    try:
        reparado = texto
        reparado = re.sub(r"'", '"', reparado)
        reparado = re.sub(r',\s*([}\]])', r'\1', reparado)
        if tipo == "objeto":
            match = re.search(r'\{[\s\S]*\}', reparado)
        else:
            match = re.search(r'\[[\s\S]*\]', reparado)
        if match:
            return json.loads(match.group())
    except Exception:
        pass

    return None

# ─────────────────────────────────────────────
#  CATALOGO
# ─────────────────────────────────────────────

def cargar_catalogo():
    try:
        with open(HABILIDADES, "r", encoding="utf-8", errors="replace") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_catalogo(catalogo):
    tmp = HABILIDADES + ".tmp"
    bak = HABILIDADES + ".bak"
    if os.path.exists(HABILIDADES):
        shutil.copy2(HABILIDADES, bak)
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(catalogo, f, indent=4, ensure_ascii=False)
    os.replace(tmp, HABILIDADES)

# ─────────────────────────────────────────────
#  PASO 1 — ANALIZAR EL NEGOCIO
# ─────────────────────────────────────────────

def analizar_negocio(descripcion):
    prompt = (
        "Eres arquitecto de sistemas de IA para empresas.\n\n"
        "DESCRIPCION DEL NEGOCIO:\n" + descripcion + "\n\n"
        "Extrae la informacion y devuelve SOLO JSON valido, sin texto extra, sin markdown:\n"
        '{"nombre":"Nombre comercial","slug":"slug_lowercase","dominio":"dominio.com",'
        '"modelo":"descripcion corta del modelo de negocio","idiomas":["es","en"],'
        '"agentes_necesarios":['
        '{"archivo":"nombre.py","funcion":"que hace exactamente","area":"AREA","critico":true}'
        ']}\n\n'
        "Lista 8-12 agentes que este negocio necesita para operar automaticamente.\n"
        "Ejemplos para agencia de viajes: cotizador_viaje.py, buscador_vuelos.py, "
        "buscador_hoteles.py, buscador_restaurantes.py, calculadora_fee.py, "
        "generador_itinerario.py, confirmador_reservas.py, seguimiento_cliente.py\n"
        "DEVUELVE SOLO EL JSON. Sin texto antes ni despues."
    )

    for intento in range(3):
        log("  Intento " + str(intento+1) + " de analisis...")
        respuesta = ia(prompt)
        if not respuesta:
            time.sleep(3)
            continue
        resultado = extraer_json(respuesta, "objeto")
        if resultado and "nombre" in resultado and "agentes_necesarios" in resultado:
            return resultado
        log("  Respuesta no parseable, reintentando...")
        time.sleep(2)

    # Fallback: construir estructura minima desde la descripcion
    log("  Usando fallback para construir estructura del negocio...")
    palabras = descripcion.lower().split()
    nombre = "Empresa"
    for i, p in enumerate(palabras):
        if p in ("llamada", "llamado", "nombre"):
            if i+1 < len(palabras):
                nombre = palabras[i+1].title()
                break

    slug = re.sub(r'[^a-z0-9]', '_', nombre.lower())

    return {
        "nombre": nombre,
        "slug": slug,
        "dominio": None,
        "modelo": descripcion[:100],
        "idiomas": ["es", "en"],
        "agentes_necesarios": [
            {"archivo": "cotizador_viaje.py", "funcion": "Cotiza viajes completos con fee del 8%", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_vuelos.py", "funcion": "Busca y compara opciones de vuelos", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_hoteles.py", "funcion": "Busca hoteles por destino y presupuesto", "area": "TURISMO", "critico": True},
            {"archivo": "buscador_restaurantes.py", "funcion": "Recomienda restaurantes por destino", "area": "TURISMO", "critico": False},
            {"archivo": "calculadora_fee_viaje.py", "funcion": "Calcula el 8% de fee sobre costo total", "area": "FINANZAS", "critico": True},
            {"archivo": "generador_itinerario.py", "funcion": "Genera itinerario dia a dia del viaje", "area": "TURISMO", "critico": True},
            {"archivo": "confirmador_reservas.py", "funcion": "Confirma y registra reservas hechas", "area": "OPERACIONES", "critico": False},
            {"archivo": "seguimiento_cliente_viaje.py", "funcion": "Da seguimiento al cliente durante el viaje", "area": "VENTAS", "critico": False},
        ]
    }

# ─────────────────────────────────────────────
#  PASO 2 — BUSCAR EN CATALOGO (logica Clawbot)
# ─────────────────────────────────────────────

def _extraer_keywords(texto):
    """Extrae keywords normalizadas de un texto para matching."""
    texto = texto.lower().replace(".py", "").replace("_", " ")
    # Quitar palabras comunes sin valor semantico
    stopwords = {"de", "del", "la", "el", "los", "las", "un", "una", "en", "para",
                 "con", "por", "que", "se", "es", "al", "y", "o", "a", "e"}
    palabras = re.findall(r'[a-z0-9]+', texto)
    return set(p for p in palabras if p not in stopwords and len(p) > 2)

def buscar_en_catalogo(agentes_necesarios, catalogo):
    """
    Busca matches por keywords entre agentes necesarios y catalogo.
    Sin LLM — comparacion directa por palabras clave compartidas.
    Match si comparten 2+ keywords relevantes.
    """
    if not catalogo:
        return [], agentes_necesarios

    # Indexar catalogo por keywords
    catalogo_index = {}
    for archivo, info in catalogo.items():
        desc = info.get("descripcion", "")
        keywords = _extraer_keywords(archivo + " " + desc)
        catalogo_index[archivo] = keywords

    reutilizar = []
    crear = []

    for ag in agentes_necesarios:
        nombre = ag.get("archivo", "")
        funcion = ag.get("funcion", "")
        keywords_necesario = _extraer_keywords(nombre + " " + funcion)

        mejor_match = None
        mejor_score = 0

        for archivo_cat, keywords_cat in catalogo_index.items():
            # Contar keywords compartidas
            comunes = keywords_necesario & keywords_cat
            score = len(comunes)
            if score > mejor_score:
                mejor_score = score
                mejor_match = archivo_cat

        # Match si comparten 2+ keywords relevantes
        if mejor_score >= 2 and mejor_match:
            reutilizar.append({
                "necesario": nombre,
                "existente": mejor_match,
                "match": f"{mejor_score} keywords comunes"
            })
        else:
            crear.append(ag)

    return reutilizar, crear

# ─────────────────────────────────────────────
#  PASO 3 — CREAR AGENTE NUEVO
# ─────────────────────────────────────────────

def limpiar_codigo(texto):
    if "```python" in texto:
        return texto.split("```python")[1].split("```")[0].strip()
    if "```" in texto:
        return texto.split("```")[1].split("```")[0].strip()
    return texto.strip()

def validar_sintaxis(codigo):
    try:
        ast.parse(codigo)
        return True, None
    except SyntaxError as e:
        return False, str(e)

def probar_agente(ruta):
    try:
        r = subprocess.run(
            [sys.executable, ruta],
            capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=60  # Fix: 60s timeout
        )
        salida = (r.stdout or "").strip()
        if len(salida) < 5:
            return False, (r.stderr or "Output vacio")[:200]
        return True, salida[:200]
    except subprocess.TimeoutExpired:
        return False, "Timeout 60s"
    except Exception as e:
        return False, str(e)

def agregar_a_misiones(archivo, funcion, area):
    """
    Agrega un agente fallido a misiones.txt en el formato que espera auto_run.py:
    archivo.py;instruccion
    """
    instruccion = f"Crear agente {area}: {funcion}"
    mision = f"{archivo};{instruccion}"
    try:
        # Leer existentes para no duplicar
        existentes = set()
        if os.path.exists(MISIONES):
            with open(MISIONES, "r", encoding="utf-8", errors="replace") as f:
                existentes = set(l.strip() for l in f if l.strip())
        if mision not in existentes:
            with open(MISIONES, "a", encoding="utf-8") as f:
                f.write(mision + "\n")
            log("  [MISION] Agregado a misiones.txt: " + archivo)
    except Exception as e:
        log("  [WARN] No se pudo agregar a misiones: " + str(e))

def crear_agente(spec, contexto_negocio):
    """Crea agente con un solo intento y timeout de 60s en la prueba."""
    prompt = (
        "Crea un agente Python autonomo para este negocio.\n\n"
        "NEGOCIO: " + contexto_negocio + "\n"
        "ARCHIVO: " + spec["archivo"] + "\n"
        "FUNCION: " + spec["funcion"] + "\n"
        "AREA: " + spec.get("area", "HERRAMIENTAS") + "\n\n"
        "REGLAS ABSOLUTAS:\n"
        "1. Encabezado con AREA, DESCRIPCION, TECNOLOGIA\n"
        "2. NUNCA input() — usa sys.argv con defaults realistas\n"
        "3. Output minimo 5 lineas con datos concretos\n"
        "4. Solo stdlib: os, sys, json, datetime, math, re, random\n"
        "5. def main() + if __name__ == '__main__': main()\n"
        "6. try/except en main()\n"
        "7. Datos especificos y utiles para el negocio\n"
        "8. Si se beneficia de datos en tiempo real, usar:\n"
        "   try:\n"
        "       import web_bridge as web\n"
        "       WEB = web.WEB\n"
        "   except ImportError:\n"
        "       WEB = False\n\n"
        "DEVUELVE SOLO CODIGO PYTHON. Sin markdown. Sin explicaciones."
    )

    # Un solo intento — si falla, va a misiones.txt
    respuesta = ia(prompt)
    if not respuesta:
        return None
    codigo = limpiar_codigo(respuesta)
    valido, err = validar_sintaxis(codigo)
    if valido:
        return codigo
    log("    Sintaxis invalida: " + str(err)[:60])
    return None

# ─────────────────────────────────────────────
#  ARMAR CARPETA DEL PROYECTO
# ─────────────────────────────────────────────

def crear_carpeta_proyecto(slug):
    ruta = os.path.join(PROYECTOS, slug)
    os.makedirs(os.path.join(ruta, "agentes"), exist_ok=True)
    os.makedirs(os.path.join(ruta, "outputs"), exist_ok=True)
    return ruta

def copiar_agente_a_proyecto(archivo, carpeta_proyecto):
    origen = os.path.join(BASE_DIR, archivo)
    destino = os.path.join(carpeta_proyecto, "agentes", os.path.basename(archivo))
    if os.path.exists(origen):
        shutil.copy2(origen, destino)
        return True
    return False

def generar_orquestador_proyecto(negocio, agentes_disponibles, carpeta):
    """
    Genera orquestador especifico usando la logica del Clawbot:
    selecciona agentes segun la consulta, los ejecuta, sintetiza.
    """
    lista_str = json.dumps(agentes_disponibles, ensure_ascii=False)

    codigo = '''"""
AREA: CEREBRO
DESCRIPCION: Orquestador de ''' + negocio["nombre"] + ''' — selecciona agentes
             segun la consulta del cliente, los ejecuta y sintetiza la respuesta.
TECNOLOGIA: llm_router, subprocess
"""

import os
import sys
import json
import subprocess
from datetime import datetime

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
NOMBRE  = "''' + negocio["nombre"] + '''"
MODELO  = "''' + negocio["modelo"] + '''"
AGENTES = ''' + lista_str + '''

def log(msg):
    print("[" + datetime.now().strftime("%H:%M:%S") + "] " + str(msg), flush=True)

def ejecutar_agente(agente, params=""):
    ruta = os.path.join(BASE, agente)
    if not os.path.exists(ruta):
        return None
    cmd = [sys.executable, ruta]
    if params:
        cmd.extend(str(p) for p in params.split() if p)
    try:
        r = subprocess.run(cmd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", timeout=30,
                          cwd=BASE)
        return (r.stdout or "").strip() or None
    except Exception as e:
        return None

def seleccionar_agentes(consulta):
    agentes_txt = "\\n".join(AGENTES)
    prompt = (
        "Eres el director de " + NOMBRE + ".\\n"
        "Negocio: " + MODELO + "\\n"
        "Consulta del cliente: " + consulta + "\\n\\n"
        "Agentes disponibles:\\n" + agentes_txt + "\\n\\n"
        "Selecciona 2-4 agentes mas utiles para esta consulta.\\n"
        "Devuelve SOLO JSON: "
        "[{\\"agente\\": \\"agentes/archivo.py\\", \\"params\\": \\"\\", \\"objetivo\\": \\"que busca\\"}]"
    )
    respuesta = ia(prompt)
    if not respuesta:
        return []
    # Extraer JSON
    import re
    match = re.search(r"\\[.*\\]", respuesta, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except Exception:
            pass
    return []

def sintetizar(consulta, resultados):
    datos = "\\n\\n".join([r["agente"] + ":\\n" + r["output"] for r in resultados])
    prompt = (
        "Eres el asistente de " + NOMBRE + ".\\n"
        "Consulta del cliente: " + consulta + "\\n\\n"
        "Datos recopilados:\\n" + datos + "\\n\\n"
        "Responde directamente al cliente con una propuesta clara y completa.\\n"
        "Incluye precios, detalles y el siguiente paso a seguir.\\n"
        "Maximo 300 palabras."
    )
    return ia(prompt) or datos

def procesar(consulta):
    log("Consulta: " + consulta[:80])

    plan = seleccionar_agentes(consulta)
    if not plan:
        log("Sin plan — respuesta directa")
        return ia("Eres asistente de " + NOMBRE + ". Responde: " + consulta)

    log("Agentes seleccionados: " + str(len(plan)))
    resultados = []

    for paso in plan:
        agente  = paso.get("agente", "")
        params  = paso.get("params", "")
        objetivo = paso.get("objetivo", "")
        log("  Ejecutando " + agente + " — " + objetivo)
        output = ejecutar_agente(agente, params)
        if output:
            resultados.append({"agente": agente, "output": output[:400]})
            log("  [OK] " + output[:60])
        else:
            log("  [SKIP] Sin output")

    if not resultados:
        return ia("Eres asistente de " + NOMBRE + ". Responde sobre: " + consulta)

    log("Sintetizando...")
    return sintetizar(consulta, resultados)

if __name__ == "__main__":
    consulta = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "hola como puedo planear un viaje"
    print("\\n" + "="*60)
    print(NOMBRE + " — Sistema de IA")
    print("="*60)
    resultado = procesar(consulta)
    print("\\n" + resultado)
    print("="*60)
'''

    ruta = os.path.join(carpeta, "orquestador.py")
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(codigo)
    log("Orquestador generado: " + ruta)
    return ruta

def generar_readme(negocio, reutilizados, creados, carpeta):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M')
    lineas = [
        "# " + negocio["nombre"] + " — Sistema de IA",
        "Generado por Agencia Santi — " + ts,
        "",
        "## Modelo de Negocio",
        negocio["modelo"],
        "",
        "## Dominio",
        str(negocio.get("dominio") or "No especificado"),
        "",
        "## Agentes Reutilizados del Catalogo (" + str(len(reutilizados)) + ")",
    ]
    for r in reutilizados:
        lineas.append("- " + r.get("existente", "") + " -> cubre: " + r.get("necesario", ""))
    lineas += ["", "## Agentes Nuevos Creados (" + str(len(creados)) + ")"]
    for c in creados:
        lineas.append("- " + c.get("archivo", ""))
    lineas += [
        "",
        "## Uso",
        "```",
        "cd proyectos/" + negocio["slug"],
        "python orquestador.py 'quiero ir a japon en marzo para 2 personas'",
        "```",
    ]
    with open(os.path.join(carpeta, "README.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lineas))

# ─────────────────────────────────────────────
#  FLUJO PRINCIPAL
# ─────────────────────────────────────────────

def crear_proyecto(descripcion):
    log("=" * 55)
    log("ORQUESTADOR DE PROYECTOS v2.0")
    log("=" * 55)

    # PASO 1: Analizar negocio
    log("Paso 1/5 — Analizando el negocio...")
    negocio = analizar_negocio(descripcion)
    if not negocio:
        log("ERROR: No pude analizar la descripcion.")
        return None

    nombre = negocio["nombre"]
    # Fix: slug limpio — quitar caracteres raros, doble underscore, trailing _
    slug_raw = negocio.get("slug", nombre)
    slug = re.sub(r'[^a-z0-9]', '_', slug_raw.lower())
    slug = re.sub(r'_+', '_', slug).strip('_')  # sin __ ni _ al inicio/final
    if not slug:
        slug = "proyecto_" + datetime.now().strftime("%Y%m%d%H%M%S")
    log("Negocio: " + nombre + " (" + slug + ")")
    log("Modelo: " + negocio["modelo"])
    log("Agentes necesarios: " + str(len(negocio["agentes_necesarios"])))

    # PASO 2: Buscar en catalogo
    log("\nPaso 2/5 — Buscando en catalogo actual...")
    catalogo = cargar_catalogo()
    log("Catalogo actual: " + str(len(catalogo)) + " agentes")

    reutilizar, crear = buscar_en_catalogo(negocio["agentes_necesarios"], catalogo)
    log("Reutilizar: " + str(len(reutilizar)) + " | Crear nuevos: " + str(len(crear)))

    for r in reutilizar:
        log("  [OK] Reutilizar " + r.get("existente", "") + " para " + r.get("necesario", ""))
    for c in crear:
        log("  [+] Crear nuevo: " + c.get("archivo", ""))

    # PASO 3: Crear carpeta
    log("\nPaso 3/5 — Creando carpeta del proyecto...")
    carpeta = crear_carpeta_proyecto(slug)
    log("Carpeta: proyectos/" + slug + "/")

    agentes_en_proyecto = []

    # Copiar reutilizados
    for r in reutilizar:
        archivo = r.get("existente", "")
        if copiar_agente_a_proyecto(archivo, carpeta):
            agentes_en_proyecto.append("agentes/" + os.path.basename(archivo))
            log("  Copiado: " + archivo)

    # PASO 4: Crear agentes nuevos
    log("\nPaso 4/5 — Creando agentes nuevos...")
    contexto = nombre + " — " + negocio["modelo"]
    agentes_creados = []

    for spec in crear:
        archivo = spec.get("archivo", "")
        if not archivo:
            continue
        log("  Creando " + archivo + "...")
        codigo = crear_agente(spec, contexto)

        if not codigo:
            log("  [ERROR] No se pudo crear " + archivo + " — enviando a misiones")
            agregar_a_misiones(archivo, spec.get("funcion", ""), spec.get("area", "HERRAMIENTAS"))
            continue

        # Guardar en proyecto
        ruta_proyecto = os.path.join(carpeta, "agentes", archivo)
        with open(ruta_proyecto, "w", encoding="utf-8") as f:
            f.write(codigo)

        # Probar con 60s timeout
        exito, output = probar_agente(ruta_proyecto)

        if not exito:
            log("  [FAIL] " + archivo + " — " + output[:60] + " — enviando a misiones")
            agregar_a_misiones(archivo, spec.get("funcion", ""), spec.get("area", "HERRAMIENTAS"))
            continue

        log("  [OK] " + archivo + " — " + output[:60])

        # Copiar al BASE_DIR y registrar en catalogo global
        ruta_global = os.path.join(BASE_DIR, archivo)
        shutil.copy2(ruta_proyecto, ruta_global)

        catalogo[archivo] = {
            "descripcion": spec.get("funcion", ""),
            "categoria": spec.get("area", "HERRAMIENTAS"),
            "salud": "OK",
            "tecnologia": ["Python estandar"],
            "ultima_actualizacion": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "ordenes": [archivo.replace(".py", "").replace("_", " ")]
        }
        agentes_creados.append(spec)
        agentes_en_proyecto.append("agentes/" + archivo)
        time.sleep(1)

    # Actualizar catalogo global
    if agentes_creados:
        guardar_catalogo(catalogo)
        log("Catalogo actualizado: +" + str(len(agentes_creados)) + " agentes nuevos")

    # PASO 5: Orquestador y README
    log("\nPaso 5/5 — Generando orquestador y README...")
    generar_orquestador_proyecto(negocio, agentes_en_proyecto, carpeta)
    generar_readme(negocio, reutilizar, agentes_creados, carpeta)

    log("\n" + "=" * 55)
    log("PROYECTO LISTO: " + nombre)
    log("Carpeta:  proyectos/" + slug + "/")
    log("Agentes reutilizados: " + str(len(reutilizar)))
    log("Agentes nuevos: " + str(len(agentes_creados)))
    log("Total en proyecto: " + str(len(agentes_en_proyecto)))
    log("=" * 55)
    log("")
    log("Para probar:")
    log("  cd proyectos/" + slug)
    log("  python orquestador.py 'quiero ir a japon en marzo 2 personas presupuesto 3000 dolares'")

    return {
        "nombre": nombre,
        "slug": slug,
        "carpeta": carpeta,
        "reutilizados": len(reutilizar),
        "creados": len(agentes_creados),
        "total": len(agentes_en_proyecto)
    }


if __name__ == "__main__":
    if len(sys.argv) > 1:
        descripcion = " ".join(sys.argv[1:])
    else:
        print("Uso: python orquestador_proyectos.py 'descripcion del negocio'")
        print("")
        print("Ejemplo:")
        print("  python orquestador_proyectos.py 'agencia de viajes Way2TheUnknown,")
        print("  cobra 8% de fee, atiende mercado mexicano e internacional'")
        sys.exit(0)

    crear_proyecto(descripcion)