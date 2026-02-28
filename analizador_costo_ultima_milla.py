"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza analizador costo ultima milla
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        distancia = 10  # km
        velocidad = 30  # km/h
        costo_combustible = 20  # pesos por litro
        consumo_combustible = 10  # litros por 100 km
        costo_mano_obra = 50  # pesos por hora
        impuestos = 0.16  # 16% de impuestos
        seguro = 0.05  # 5% de seguro

        # Opciones de línea de comandos
        if len(sys.argv) > 1:
            distancia = int(sys.argv[1])
        if len(sys.argv) > 2:
            velocidad = int(sys.argv[2])
        if len(sys.argv) > 3:
            costo_combustible = int(sys.argv[3])
        if len(sys.argv) > 4:
            consumo_combustible = int(sys.argv[4])
        if len(sys.argv) > 5:
            costo_mano_obra = int(sys.argv[5])

        # Cálculo del costo de la última milla
        tiempo_recorrido = distancia / velocidad
        costo_combustible_total = (distancia / 100) * consumo_combustible * costo_combustible
        costo_mano_obra_total = tiempo_recorrido * costo_mano_obra
        costo_impuestos = (costo_combustible_total + costo_mano_obra_total) * impuestos
        costo_seguro = (costo_combustible_total + costo_mano_obra_total) * seguro
        costo_total = costo_combustible_total + costo_mano_obra_total + costo_impuestos + costo_seguro

        print(f"Distancia recorrida: {distancia} km")
        print(f"Velocidad promedio: {velocidad} km/h")
        print(f"Costo del combustible: ${costo_combustible_total:.2f} MXN")
        print(f"Costo de la mano de obra: ${costo_mano_obra_total:.2f} MXN")
        print(f"Tiempo recorrido: {tiempo_recorrido:.2f} horas")
        print(f"Costo de impuestos: ${costo_impuestos:.2f} MXN")
        print(f"Costo de seguro: ${costo_seguro:.2f} MXN")
        print(f"Costo total de la última milla: ${costo_total:.2f} MXN")
        print(f"Costo por kilómetro: ${costo_total / distancia:.2f} MXN/km")
        print(f"Fecha y hora del cálculo: {datetime.datetime.now()}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El costo total de la última milla es de ${costo_total:.2f} MXN, con un costo por kilómetro de ${costo_total / distancia:.2f} MXN/km.")
        print(f"El tiempo recorrido es de {tiempo_recorrido:.2f} horas, con una velocidad promedio de {velocidad} km/h.")
        print(f"El costo de impuestos y seguro es de ${costo_impuestos + costo_seguro:.2f} MXN, lo que representa un {((costo_impuestos + costo_seguro) / costo_total) * 100:.2f}% del costo total.")

    except ValueError as e:
        print(f"Error: {e}. Por favor, ingrese valores numéricos.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()