import sys
import json
import datetime
import math
import re
import random
import os

def calcular_precio_promedio(zona):
    zonas_precios = {
        "Zona Rosa": [12000000, 15000000, 18000000, 20000000, 22000000],
        "Polanco": [18000000, 22000000, 25000000, 28000000, 30000000],
        "Condesa": [15000000, 18000000, 20000000, 22000000, 24000000],
        "Santa Fe": [20000000, 25000000, 28000000, 32000000, 35000000],
        "Reforma": [16000000, 20000000, 23000000, 26000000, 28000000],
        "Coyoacán": [10000000, 13000000, 16000000, 18000000, 20000000]
    }

    precios = zonas_precios.get(zona.lower(), [10000000, 12000000, 14000000, 16000000, 18000000])
    return sum(precios) / len(precios)

def calcular_alquiler_promedio(zona):
    zonas_alquileres = {
        "Zona Rosa": [80000, 100000, 120000, 150000, 180000],
        "Polanco": [120000, 150000, 180000, 220000, 250000],
        "Condesa": [90000, 120000, 150000, 180000, 200000],
        "Santa Fe": [150000, 180000, 220000, 250000, 300000],
        "Reforma": [100000, 130000, 160000, 190000, 220000],
        "Coyoacán": [60000, 80000, 100000, 120000, 150000]
    }

    alquileres = zonas_alquileres.get(zona.lower(), [70000, 90000, 110000, 130000, 150000])
    return sum(alquileres) / len(alquileres)

def calcular_rotacion(zona):
    return random.uniform(0.8, 1.2)

def calcular_tendencia(zona):
    return random.choice(["Alta", "Media", "Baja"])

def obtener_datos_zona(zona):
    try:
        datos = {
            "zona": zona,
            "precio_promedio": calcular_precio_promedio(zona),
            "alquiler_promedio": calcular_alquiler_promedio(zona),
            "rotacion": calcular_rotacion(zona),
            "tendencia": calcular_tendencia(zona)
        }
        return datos
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

def main():
    if len(sys.argv) > 1:
        zona = sys.argv[1]
    else:
        zona = "Zona Rosa"

    datos = obtener_datos_zona(zona)
    if datos:
        print(f"Zona: {datos['zona']}")
        print(f"Precio promedio: ${datos['precio_promedio']:.2f}")
        print(f"Alquiler promedio: ${datos['alquiler_promedio']:.2f}")
        print(f"Rotación: {datos['rotacion']:.2f}")
        print(f"Tendencia: {datos['tendencia']}")

        print("\nResumen Ejecutivo:")
        print(f"La zona {datos['zona']} tiene un precio promedio de ${datos['precio_promedio']:.2f} y un alquiler promedio de ${datos['alquiler_promedio']:.2f}.")
        print(f"La rotación en esta zona es de {datos['rotacion']:.2f} y la tendencia es {datos['tendencia']}.")
    else:
        print("No se pudo obtener información para la zona solicitada.")

if __name__ == "__main__":
    main()