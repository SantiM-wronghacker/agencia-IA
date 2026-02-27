# MANUFACTURA/ANALIZADOR CAPACIDAD PLANTA/PYTHON

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Obtener argumentos de la linea de comandos
        capacidad_planta = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
        produccion_diaria = int(sys.argv[2]) if len(sys.argv) > 2 else 500
        horas_trabajo = int(sys.argv[3]) if len(sys.argv) > 3 else 8

        # Calcular capacidad total de la planta
        capacidad_total = capacidad_planta * horas_trabajo

        # Calcular porcentaje de capacidad utilizada
        porcentaje_capacidad_utilizada = (produccion_diaria / capacidad_total) * 100

        # Calcular tiempo de entrega promedio
        tiempo_entrega_promedio = random.uniform(1, 5)

        # Calcular costo de produccion por unidad
        costo_produccion_por_unidad = random.uniform(100, 500)

        # Imprimir resultados
        print(f"Capacidad total de la planta: {capacidad_total} unidades")
        print(f"Produccion diaria: {produccion_diaria} unidades")
        print(f"Porcentaje de capacidad utilizada: {porcentaje_capacidad_utilizada:.2f}%")
        print(f"Tiempo de entrega promedio: {tiempo_entrega_promedio:.2f} dias")
        print(f"Costo de produccion por unidad: ${costo_produccion_por_unidad:.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()