# CEREBRO/Clasificador de prioridad de tareas/Python

import sys
import json
import datetime
import math
import re
import random
import os

def clasificar_prioridad(tarea):
    prioridades = {
        'alta': 1,
        'media': 2,
        'baja': 3
    }
    return prioridades.get(tarea['prioridad'], 3)

def main():
    try:
        if len(sys.argv) > 1:
            archivo_tareas = sys.argv[1]
        else:
            archivo_tareas = 'tareas.json'

        if not os.path.exists(archivo_tareas):
            print("Archivo de tareas no encontrado")
            return

        with open(archivo_tareas, 'r') as f:
            tareas = json.load(f)

        tareas_clasificadas = []
        for tarea in tareas:
            prioridad = clasificar_prioridad(tarea)
            tarea['prioridad_numerica'] = prioridad
            tareas_clasificadas.append(tarea)

        tareas_clasificadas.sort(key=lambda x: x['prioridad_numerica'])

        for i, tarea in enumerate(tareas_clasificadas):
            print(f"Tarea {i+1}: {tarea['nombre']} - Prioridad: {tarea['prioridad']} - Fecha de vencimiento: {tarea['fecha_vencimiento']}")
            print(f"Descripción: {tarea['descripcion']}")
            print(f"Prioridad numérica: {tarea['prioridad_numerica']}")
            print(f"Tiempo estimado: {tarea['tiempo_estimado']} horas")
            print(f"Costo estimado: ${tarea['costo_estimado']:.2f} MXN")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()