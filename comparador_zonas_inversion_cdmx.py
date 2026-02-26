"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza comparador zonas inversion cdmx
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Definir zonas de inversión en la CDMX
        zonas = {
            "Polanco": {"precio_m2": 150000, "renta_mensual": 30000},
            "Reforma": {"precio_m2": 120000, "renta_mensual": 25000},
            "Condesa": {"precio_m2": 100000, "renta_mensual": 20000},
            "Roma": {"precio_m2": 90000, "renta_mensual": 18000},
            "Juárez": {"precio_m2": 80000, "renta_mensual": 15000},
        }

        # Definir argumentos por defecto
        zona1 = "Polanco"
        zona2 = "Reforma"

        # Verificar argumentos
        if len(sys.argv) > 1:
            zona1 = sys.argv[1]
        if len(sys.argv) > 2:
            zona2 = sys.argv[2]

        # Verificar si las zonas existen
        if zona1 not in zonas or zona2 not in zonas:
            print("Error: Zona no existe")
            return

        # Calcular diferencia de precio por metro cuadrado
        diff_precio_m2 = zonas[zona1]["precio_m2"] - zonas[zona2]["precio_m2"]

        # Calcular diferencia de renta mensual
        diff_renta_mensual = zonas[zona1]["renta_mensual"] - zonas[zona2]["renta_mensual"]

        # Calcular relación precio-renta
        relacion_precio_renta1 = zonas[zona1]["precio_m2"] / zonas[zona1]["renta_mensual"]
        relacion_precio_renta2 = zonas[zona2]["precio_m2"] / zonas[zona2]["renta_mensual"]

        # Imprimir resultados
        print(f"Zona 1: {zona1}")
        print(f"Zona 2: {zona2}")
        print(f"Diferencia de precio por metro cuadrado: {diff_precio_m2} MXN")
        print(f"Diferencia de renta mensual: {diff_renta_mensual} MXN")
        print(f"Relación precio-renta en {zona1}: {relacion_precio_renta1:.2f}")
        print(f"Relación precio-renta en {zona2}: {relacion_precio_renta2:.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()