# CEREBRO/Clasificador de prioridad de tareas/Python
# AREA: CEREBRO
# DESCRIPCION: Agente que realiza clasificador prioridad tareas
# TECNOLOGIA: Python

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

def clasificar_prioridad(tarea):
    prioridades = {
        'alta': 1,
        'media': 2,
        'baja': 3
    }
    return prioridades.get(tarea['prioridad'], 3)

def calcular_tiempo_estimado(tarea):
    try:
        return float(tarea['tiempo_estimado'])
    except (ValueError, KeyError):
        return 0.0

def calcular_costo_estimado(tarea):
    try:
        return float(tarea['costo_estimado'])
    except (ValueError, KeyError):
        return 0.0

def calcular_fecha_vencimiento(tarea):
    try:
        return datetime.datetime.strptime(tarea['fecha_vencimiento'], '%Y-%m-%d')
    except (ValueError, KeyError):
        return datetime.datetime.now()

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
            tarea['tiempo_estimado_horas'] = calcular_tiempo_estimado(tarea)
            tarea['costo_estimado_mxn'] = calcular_costo_estimado(tarea)
            tarea['fecha_vencimiento_date'] = calcular_fecha_vencimiento(tarea)
            tareas_clasificadas.append(tarea)

        tareas_clasificadas.sort(key=lambda x: x['prioridad_numerica'])

        for i, tarea in enumerate(tareas_clasificadas):
            print(f"Tarea {i+1}: {tarea.get('nombre', 'Sin nombre')} - Prioridad: {tarea.get('prioridad', 'Sin prioridad')} - Fecha de vencimiento: {tarea.get('fecha_vencimiento', 'Sin fecha de vencimiento')}")
            print(f"Descripción: {tarea.get('descripcion', 'Sin descripción')}")
            print(f"Tiempo estimado: {tarea['tiempo_estimado_horas']} horas")
            print(f"Costo estimado: ${tarea['costo_estimado_mxn']:.2f} MXN")
            print(f"Fecha de vencimiento (datetime): {tarea['fecha_vencimiento_date']}")
            print("-" * 50)

        print("Resumen ejecutivo:")
        print(f"Total de tareas: {len(tareas_clasificadas)}")
        print(f"Tareas con prioridad alta: {len([t for t in tareas_clasificadas if t['prioridad_numerica'] == 1])}")
        print(f"Tareas con prioridad media: {len([t for t in tareas_clasificadas if t['prioridad_numerica'] == 2])}")
        print(f"Tareas con prioridad baja: {len([t for t in tareas_clasificadas if t['prioridad_numerica'] == 3])}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()