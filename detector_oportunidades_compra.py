"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza detector oportunidades compra
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
        ciudad = sys.argv[1] if len(sys.argv) > 1 else "Ciudad de México"
        estado = sys.argv[2] if len(sys.argv) > 2 else "CDMX"
        presupuesto = int(sys.argv[3]) if len(sys.argv) > 3 else 5000000

        # Generar oportunidades de compra
        oportunidades = []
        for _ in range(5):
            precio = random.randint(presupuesto * 0.8, presupuesto * 1.2)
            metros_cuadrados = random.randint(50, 200)
            habitaciones = random.randint(2, 5)
            banos = random.randint(1, 3)
            colonia = random.choice(["Condesa", "Roma", "Juárez", "Cuauhtémoc", "Miguel Hidalgo"])
            oportunidades.append({
                "ciudad": ciudad,
                "estado": estado,
                "precio": precio,
                "metros_cuadrados": metros_cuadrados,
                "habitaciones": habitaciones,
                "banos": banos,
                "colonia": colonia
            })

        # Imprimir oportunidades
        for i, oportunidad in enumerate(oportunidades):
            print(f"Oportunidad {i+1}:")
            print(f"Ciudad: {oportunidad['ciudad']}")
            print(f"Estado: {oportunidad['estado']}")
            print(f"Precio: ${oportunidad['precio']:,}")
            print(f"Metros cuadrados: {oportunidad['metros_cuadrados']}")
            print(f"Habitaciones: {oportunidad['habitaciones']}")
            print(f"Banos: {oportunidad['banos']}")
            print(f"Colonia: {oportunidad['colonia']}\n")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()