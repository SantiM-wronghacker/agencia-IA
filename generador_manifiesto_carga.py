"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza generador manifiesto carga
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
        fecha_inicial = datetime.date.today()
        fecha_final = datetime.date.today() + datetime.timedelta(days=7)
        cantidad_cargas = 10

        # Parámetros desde línea de comandos
        if len(sys.argv) > 1:
            fecha_inicial = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        if len(sys.argv) > 2:
            fecha_final = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        if len(sys.argv) > 3:
            cantidad_cargas = int(sys.argv[3])

        # Generar manifiesto de carga
        manifiesto = []
        for i in range(cantidad_cargas):
            carga = {
                "id": i+1,
                "fecha": (fecha_inicial + datetime.timedelta(days=random.randint(0, (fecha_final - fecha_inicial).days))).isoformat(),
                "origen": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "destino": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "peso": round(random.uniform(100, 1000), 2),
                "valor": round(random.uniform(1000, 10000), 2)
            }
            manifiesto.append(carga)

        # Imprimir manifiesto
        print("Manifiesto de Carga:")
        for carga in manifiesto:
            print(f"ID: {carga['id']}")
            print(f"Fecha: {carga['fecha']}")
            print(f"Origen: {carga['origen']}")
            print(f"Destino: {carga['destino']}")
            print(f"Peso: {carga['peso']} kg")
            print(f"Valor: ${carga['valor']:.2f} MXN")
            print("-" * 50)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()