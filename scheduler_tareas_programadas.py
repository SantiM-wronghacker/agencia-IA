"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza scheduler tareas programadas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import os
import math
import re
import random

def main():
    try:
        # Configuración de tareas programadas
        if len(sys.argv) > 1:
            tareas = json.loads(sys.argv[1])
        else:
            tareas = [
                {"nombre": "Tarea 1", "hora": 8, "minuto": 0, "duracion": 30},
                {"nombre": "Tarea 2", "hora": 12, "minuto": 30, "duracion": 60},
                {"nombre": "Tarea 3", "hora": 16, "minuto": 0, "duracion": 45},
            ]

        # Fecha y hora actual
        ahora = datetime.datetime.now()
        print(f"Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")

        # Listado de tareas programadas
        print("Tareas programadas:")
        tareas_ejecutadas = 0
        for i, tarea in enumerate(tareas, 1):
            print(f"{i}. {tarea['nombre']} a las {tarea['hora']}:{tarea['minuto']:02d} durante {tarea['duracion']} minutos")
            if ahora.hour == tarea["hora"] and ahora.minute == tarea["minuto"]:
                print(f"  - Estado: Ejecutando")
                tareas_ejecutadas += 1
            elif ahora.hour > tarea["hora"] or (ahora.hour == tarea["hora"] and ahora.minute > tarea["minuto"]):
                print(f"  - Estado: Ya ejecutada")
            else:
                print(f"  - Estado: Pendiente de ejecución")
            proxima_ejecucion = datetime.datetime.now()
            proxima_ejecucion = proxima_ejecucion.replace(hour=tarea["hora"], minute=tarea["minuto"], second=0)
            if proxima_ejecucion < datetime.datetime.now():
                proxima_ejecucion += datetime.timedelta(days=1)
            tiempo_restante = proxima_ejecucion - datetime.datetime.now()
            print(f"  - Tiempo restante para la próxima ejecución: {tiempo_restante}")

        # Estadísticas de tareas
        print("\nEstadísticas de tareas:")
        total_tareas = len(tareas)
        tareas_pendientes = total_tareas - tareas_ejecutadas
        print(f"Total de tareas: {total_tareas}")
        print(f"Tareas ejecutadas: {tareas_ejecutadas}")
        print(f"Tareas pendientes: {tareas_pendientes}")
        print(f"Porcentaje de tareas ejecutadas: {(tareas_ejecutadas / total_tareas) * 100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"Fecha y hora actual: {ahora.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total de tareas: {total_tareas}")
        print(f"Tareas ejecutadas: {tareas_ejecutadas}")
        print(f"Tareas pendientes: {tareas_pendientes}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()