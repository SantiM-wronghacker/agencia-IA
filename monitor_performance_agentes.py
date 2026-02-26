"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza monitor performance agentes
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
        num_agentes = 10
        tiempo_monitoreo = 60  # en segundos

        # Obtener parámetros desde la línea de comandos
        if len(sys.argv) > 1:
            num_agentes = int(sys.argv[1])
        if len(sys.argv) > 2:
            tiempo_monitoreo = int(sys.argv[2])

        # Simular datos de monitoreo
        datos_monitoreo = []
        for i in range(num_agentes):
            datos = {
                "agente": f"Agente {i+1}",
                "tiempo_respuesta": round(random.uniform(0.1, 2.0), 2),  # en segundos
                "memoria_usada": round(random.uniform(100, 500), 2),  # en MB
                "cpu_usada": round(random.uniform(10, 90), 2)  # en porcentaje
            }
            datos_monitoreo.append(datos)

        # Imprimir resultados
        print(f"Fecha y hora de monitoreo: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Tiempo de monitoreo: {tiempo_monitoreo} segundos")
        print(f"Número de agentes: {num_agentes}")
        print("Datos de monitoreo:")
        for datos in datos_monitoreo:
            print(f"  - {datos['agente']}:")
            print(f"    * Tiempo de respuesta: {datos['tiempo_respuesta']} segundos")
            print(f"    * Memoria usada: {datos['memoria_usada']} MB")
            print(f"    * CPU usada: {datos['cpu_usada']}%")
        print(f"Monitoreo finalizado con éxito")

    except Exception as e:
        print(f"Error durante el monitoreo: {str(e)}")

if __name__ == "__main__":
    main()