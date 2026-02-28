"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Genera un resumen ejecutivo diario basado en logs de eventos
TECNOLOGÍA: Python, json, RootAssistant
"""
import json
import sys
from datetime import datetime
from root_assistant import RootAssistant
import time
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_resumen_ejecutivo(ruta_log="runs/state.json"):
    try:
        with open(ruta_log, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: Archivo de logs no encontrado. Verifica la ruta.")
        return
    except json.JSONDecodeError:
        print("Error: Formato JSON inválido en el archivo de logs.")
        return
    except Exception as e:
        print(f"Error inesperado al leer logs: {e}")
        return

    hoy = datetime.now().strftime("%Y-%m-%d")
    eventos_hoy = [e for e in data.get('recent', []) if e.get('timestamp') and hoy in e['timestamp']]

    if not eventos_hoy:
        print(f"No hay actividad para hoy ({hoy}).")
        return

    eventos_resumidos = eventos_hoy[-15:]
    texto_logs = json.dumps(eventos_resumidos, indent=2)

    prompt_reporte = f"""
    Eres el Director de Operaciones. Redacta un RESUMEN EJECUTIVO para Santi.
    Eventos analizados: {len(eventos_resumidos)} de {len(eventos_hoy)}.
    Prioriza información relevante para operaciones en México.

    LOGS DE HOY:
    {texto_logs}

    FORMATO:
    1. Logros: Avances significativos, metas cumplidas
    2. Conocimiento: Nuevos datos o aprendizajes
    3. Salud del sistema: Estado técnico y posibles riesgos
    4. Recomendaciones: Acciones prioritarias para el equipo
    """

    print(f"Analizando {len(eventos_resumidos)} eventos con la IA...")
    ra = RootAssistant()

    resultado = ra.process_query(prompt_reporte)
    time.sleep(2)

    if resultado and isinstance(resultado, tuple):
        resumen = resultado[0]
    else:
        resumen = "La IA no pudo generar el reporte (posible saturación de memoria o falta de API)."

    filename = f"reporte_{hoy}.txt"
    try:
        with open(filename, "w", encoding='utf-8') as f:
            f.write(str(resumen))
    except Exception as e:
        print(f"Error al guardar el reporte: {e}")
        return

    print("\n" + "="*40 + "\n REPORTE DE EVOLUCIÓN\n" + "="*40)
    print(resumen)

    # Resumen ejecutivo adicional
    print("\n=== RESUMEN EJECUTIVO ===")
    print(f"Fecha: {hoy}")
    print(f"Eventos procesados: {len(eventos_resumidos)}/{len(eventos_hoy)}")
    print(f"Estado del sistema: {'Óptimo' if 'error' not in resumen.lower() else 'Requiere atención'}")
    print(f"Recomendaciones clave: {resumen.split('Recomendaciones:')[1].split('\n')[0] if 'Recomendaciones:' in resumen else 'Ninguna recomendación especial'}")

if __name__ == "__main__":
    ruta_log = sys.argv[1] if len(sys.argv) > 1 else "runs/state.json"
    generar_resumen_ejecutivo(ruta_log)