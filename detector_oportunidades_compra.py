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
            precio = random.randint(presupuesto * 8 // 10, presupuesto * 12 // 10)
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
                "colonia": colonia,
                "antiguedad": random.randint(1, 20),
                "estado_conserva": random.choice(["Excelente", "Bueno", "Regular", "Mal"])
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
            print(f"Colonia: {oportunidad['colonia']}")
            print(f"Antiguedad: {oportunidad['antiguedad']} años")
            print(f"Estado de conserva: {oportunidad['estado_conserva']}\n")

        # Resumen ejecutivo
        print("Resumen Ejecutivo:")
        print(f"Total de oportunidades: {len(oportunidades)}")
        print(f"Precio promedio: ${sum(oportunidad['precio'] for oportunidad in oportunidades) // len(oportunidades):,}")
        print(f"Metros cuadrados promedio: {sum(oportunidad['metros_cuadrados'] for oportunidad in oportunidades) // len(oportunidades)}")
        print(f"Habitaciones promedio: {sum(oportunidad['habitaciones'] for oportunidad in oportunidades) // len(oportunidades)}")
        print(f"Banos promedio: {sum(oportunidad['banos'] for oportunidad in oportunidades) // len(oportunidades)}")

    except IndexError:
        print("Error: Debe proporcionar los parámetros ciudad, estado y presupuesto")
    except ValueError:
        print("Error: El presupuesto debe ser un número entero")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()