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

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexión a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        fecha_inicial = datetime.date.today()
        fecha_final = datetime.date.today() + datetime.timedelta(days=7)
        cantidad_cargas = 10
        impuesto = 0.16  # IVA en México

        # Parámetros desde línea de comandos
        if len(sys.argv) > 1:
            fecha_inicial = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        if len(sys.argv) > 2:
            fecha_final = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        if len(sys.argv) > 3:
            cantidad_cargas = int(sys.argv[3])
        if len(sys.argv) > 4:
            impuesto = float(sys.argv[4])

        # Generar manifiesto de carga
        manifiesto = []
        for i in range(cantidad_cargas):
            carga = {
                "id": i+1,
                "fecha": (fecha_inicial + datetime.timedelta(days=random.randint(0, (fecha_final - fecha_inicial).days))).isoformat(),
                "origen": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "destino": random.choice(["Ciudad de México", "Guadalajara", "Monterrey"]),
                "peso": round(random.uniform(100, 1000), 2),
                "valor": round(random.uniform(1000, 10000), 2),
                "impuesto": round(random.uniform(1000, 10000) * impuesto, 2),
                "total": round(random.uniform(1000, 10000) + random.uniform(1000, 10000) * impuesto, 2),
                "descripcion": f"Carga de {random.choice(['electrónicos', 'textiles', 'alimentos'])} con un peso de {round(random.uniform(100, 1000), 2)} kg",
                "transporte": random.choice(["Tren", "Camión", "Avión"]),
                "conductor": f"Conductor {random.randint(1, 10000)}",
                "vehiculo": f"Vehículo {random.randint(1, 10000)}"
            }
            manifiesto.append(carga)

        # Imprimir manifiesto
        print("# Manifiesto de Carga")
        print(f"Fecha inicial: {fecha_inicial}")
        print(f"Fecha final: {fecha_final}")
        print(f"Cantidad de cargas: {cantidad_cargas}")
        print(f"Impuesto: {impuesto*100}%")
        print()
        print("# Detalle de Cargas")
        for carga in manifiesto:
            print(f"ID: {carga['id']}")
            print(f"Fecha: {carga['fecha']}")
            print(f"Origen: {carga['origen']}")
            print(f"Destino: {carga['destino']}")
            print(f"Peso: {carga['peso']} kg")
            print(f"Valor: ${carga['valor']}")
            print(f"Impuesto: ${carga['impuesto']}")
            print(f"Total: ${carga['total']}")
            print(f"Descripción: {carga['descripcion']}")
            print(f"Transporte: {carga['transporte']}")
            print(f"Conductor: {carga['conductor']}")
            print(f"Vehículo: {carga['vehiculo']}")
            print()
        print("# Resumen Ejecutivo")
        print(f"Cantidad de cargas generadas: {len(manifiesto)}")
        print(f"Total de peso: {sum(carga['peso'] for carga in manifiesto)} kg")
        print(f"Total de valor: ${sum(carga['valor'] for carga in manifiesto)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()