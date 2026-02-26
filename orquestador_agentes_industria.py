"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza orquestador agentes industria
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Obteniendo argumentos de la línea de comandos
        if len(sys.argv) > 1:
            num_agentes = int(sys.argv[1])
            num_tareas = int(sys.argv[2])
        else:
            num_agentes = 5
            num_tareas = 10

        # Simulación de agentes y tareas
        agentes = []
        for i in range(num_agentes):
            agente = {
                "id": i,
                "tareas": []
            }
            agentes.append(agente)

        for i in range(num_tareas):
            tarea = {
                "id": i,
                "descripcion": f"Tarea {i}",
                "tiempo_estimado": random.uniform(1, 10)
            }
            agente_asignado = random.choice(agentes)
            agente_asignado["tareas"].append(tarea)

        # Imprimiendo resultados
        print(f"Fecha y hora actual: {datetime.datetime.now()}")
        print(f"Número de agentes: {num_agentes}")
        print(f"Número de tareas: {num_tareas}")
        print(f"Agentes y tareas asignadas:")
        for agente in agentes:
            print(f"Agente {agente['id']}: {len(agente['tareas'])} tareas")
            for tarea in agente["tareas"]:
                print(f"  - Tarea {tarea['id']}: {tarea['descripcion']} (Tiempo estimado: {tarea['tiempo_estimado']} horas)")

        # Estadísticas
        total_tareas = sum(len(agente["tareas"]) for agente in agentes)
        total_tiempo_estimado = sum(sum(tarea["tiempo_estimado"] for tarea in agente["tareas"]) for agente in agentes)
        print(f"Total de tareas: {total_tareas}")
        print(f"Tiempo total estimado: {total_tiempo_estimado} horas")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()