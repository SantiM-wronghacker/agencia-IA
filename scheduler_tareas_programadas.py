"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza scheduler tareas programadas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración de tareas programadas
        if len(sys.argv) > 1:
            tareas = json.loads(sys.argv[1])
        else:
            tareas = [
                {"nombre": "Tarea 1", "hora": 8, "minuto": 0},
                {"nombre": "Tarea 2", "hora": 12, "minuto": 30},
                {"nombre": "Tarea 3", "hora": 16, "minuto": 0},
            ]

        # Fecha y hora actual
        ahora = datetime.datetime.now()
        print(f"Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

        # Listado de tareas programadas
        print("Tareas programadas:")
        for tarea in tareas:
            print(f"- {tarea['nombre']} a las {tarea['hora']}:{tarea['minuto']:02d}")

        # Simulación de ejecución de tareas
        print("\nEjecución de tareas:")
        for tarea in tareas:
            if ahora.hour == tarea["hora"] and ahora.minute == tarea["minuto"]:
                print(f"- Ejecutando {tarea['nombre']}")

        # Estadísticas de tareas
        print("\nEstadísticas de tareas:")
        total_tareas = len(tareas)
        tareas_ejecutadas = 0
        tareas_pendientes = 0
        for tarea in tareas:
            if ahora.hour > tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute > tarea["minuto"]):
                tareas_ejecutadas += 1
            elif ahora.hour < tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute < tarea["minuto"]):
                tareas_pendientes += 1
        print(f"- Total de tareas: {total_tareas}")
        print(f"- Tareas ejecutadas: {tareas_ejecutadas}")
        print(f"- Tareas pendientes: {tareas_pendientes}")
        print(f"- Porcentaje de tareas ejecutadas: {(tareas_ejecutadas / total_tareas) * 100 if total_tareas > 0 else 0:.2f}%")
        print(f"- Porcentaje de tareas pendientes: {(tareas_pendientes / total_tareas) * 100 if total_tareas > 0 else 0:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"- Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"- Total de tareas: {total_tareas}")
        print(f"- Tareas ejecutadas: {tareas_ejecutadas}")
        print(f"- Tareas pendientes: {tareas_pendientes}")

    except Exception as e:
        print(f"Error: {e}")
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")

if __name__ == "__main__":
    main()