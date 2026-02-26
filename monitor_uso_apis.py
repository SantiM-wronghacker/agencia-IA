"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza monitor uso apis
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
        # Parámetros por defecto
        fecha_inicio = datetime.datetime.now() - datetime.timedelta(days=30)
        fecha_fin = datetime.datetime.now()
        umbral_alerta = 1000

        # Lectura de parámetros desde sys.argv
        if len(sys.argv) > 1:
            fecha_inicio = datetime.datetime.strptime(sys.argv[1], '%Y-%m-%d')
        if len(sys.argv) > 2:
            fecha_fin = datetime.datetime.strptime(sys.argv[2], '%Y-%m-%d')
        if len(sys.argv) > 3:
            umbral_alerta = int(sys.argv[3])

        # Simulación de uso de APIs
        uso_apis = {
            'api1': random.randint(500, 2000),
            'api2': random.randint(500, 2000),
            'api3': random.randint(500, 2000)
        }

        # Cálculo de estadísticas
        total_uso = sum(uso_apis.values())
        promedio_uso = total_uso / len(uso_apis)

        # Imprimir resultados
        print(f"Fecha de inicio: {fecha_inicio.strftime('%Y-%m-%d')}")
        print(f"Fecha de fin: {fecha_fin.strftime('%Y-%m-%d')}")
        print(f"Uso total de APIs: {total_uso} llamadas")
        print(f"Uso promedio por API: {promedio_uso:.2f} llamadas")
        print(f"Umbral de alerta: {umbral_alerta} llamadas")

        # Verificar si se supera el umbral de alerta
        if total_uso > umbral_alerta:
            print(f"ALERTA: Uso total de APIs supera el umbral de {umbral_alerta} llamadas")
        else:
            print(f"Uso total de APIs dentro del umbral de {umbral_alerta} llamadas")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()