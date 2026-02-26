"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza comparador zonas comerciales
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def calcular_precio_promedio(zona):
    precios = [100000, 200000, 300000, 400000, 500000]
    return sum(precios) / len(precios)

def calcular_alquiler_promedio(zona):
    alquileres = [5000, 10000, 15000, 20000, 25000]
    return sum(alquileres) / len(alquileres)

def obtener_datos_zona(zona):
    datos = {
        "zona": zona,
        "precio_promedio": calcular_precio_promedio(zona),
        "alquiler_promedio": calcular_alquiler_promedio(zona)
    }
    return datos

def main():
    try:
        zona1 = sys.argv[1] if len(sys.argv) > 1 else "Zona Rosa"
        zona2 = sys.argv[2] if len(sys.argv) > 2 else "Polanco"
        zona3 = sys.argv[3] if len(sys.argv) > 3 else "Condesa"

        datos_zona1 = obtener_datos_zona(zona1)
        datos_zona2 = obtener_datos_zona(zona2)
        datos_zona3 = obtener_datos_zona(zona3)

        print(f"Zona: {datos_zona1['zona']}, Precio promedio: ${datos_zona1['precio_promedio']:.2f}, Alquiler promedio: ${datos_zona1['alquiler_promedio']:.2f}")
        print(f"Zona: {datos_zona2['zona']}, Precio promedio: ${datos_zona2['precio_promedio']:.2f}, Alquiler promedio: ${datos_zona2['alquiler_promedio']:.2f}")
        print(f"Zona: {datos_zona3['zona']}, Precio promedio: ${datos_zona3['precio_promedio']:.2f}, Alquiler promedio: ${datos_zona3['alquiler_promedio']:.2f}")
        print(f"Diferencia de precio promedio entre {zona1} y {zona2}: ${abs(datos_zona1['precio_promedio'] - datos_zona2['precio_promedio']):.2f}")
        print(f"Diferencia de alquiler promedio entre {zona2} y {zona3}: ${abs(datos_zona2['alquiler_promedio'] - datos_zona3['alquiler_promedio']):.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()