"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza comparador seguros auto
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def calcular_precio_seguro(marca, modelo, año, kilometraje):
    precio_base = 5000
    ajuste_marca = {
        "Toyota": 1.1,
        "Honda": 1.05,
        "Volkswagen": 1.0,
        "Nissan": 0.95,
        "Ford": 0.9
    }
    ajuste_modelo = {
        "Sedan": 1.0,
        "Hatchback": 0.9,
        "SUV": 1.1,
        "Camioneta": 1.2
    }
    ajuste_año = 1 - (datetime.datetime.now().year - año) * 0.05
    ajuste_kilometraje = 1 - (kilometraje / 100000) * 0.1
    precio_seguro = precio_base * ajuste_marca.get(marca, 1.0) * ajuste_modelo.get(modelo, 1.0) * ajuste_año * ajuste_kilometraje
    return precio_seguro

def comparar_seguros(marca, modelo, año, kilometraje):
    seguros = [
        {"nombre": "Seguro Azteca", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje) * 1.05},
        {"nombre": "Seguro Banamex", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje) * 1.10},
        {"nombre": "Seguro Inbursa", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje) * 1.15},
        {"nombre": "Seguro Mapfre", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje) * 1.20},
        {"nombre": "Seguro GNP", "precio": calcular_precio_seguro(marca, modelo, año, kilometraje) * 1.25}
    ]
    return seguros

def main():
    try:
        marca = sys.argv[1] if len(sys.argv) > 1 else "Toyota"
        modelo = sys.argv[2] if len(sys.argv) > 2 else "Sedan"
        año = int(sys.argv[3]) if len(sys.argv) > 3 else 2020
        kilometraje = int(sys.argv[4]) if len(sys.argv) > 4 else 50000
        seguros = comparar_seguros(marca, modelo, año, kilometraje)
        print(f"Comparación de seguros para {marca} {modelo} {año} con {kilometraje} km:")
        for i, seguro in enumerate(seguros):
            print(f"{i+1}. {seguro['nombre']}: ${seguro['precio']:.2f} MXN")
        print(f"Seguro más barato: {min(seguros, key=lambda x: x['precio'])['nombre']} con un precio de ${min(seguros, key=lambda x: x['precio'])['precio']:.2f} MXN")
        print(f"Seguro más caro: {max(seguros, key=lambda x: x['precio'])['nombre']} con un precio de ${max(seguros, key=lambda x: x['precio'])['precio']:.2f} MXN")
        print(f"Diferencia entre el seguro más caro y el más barato: ${max(seguros, key=lambda x: x['precio'])['precio'] - min(seguros, key=lambda x: x['precio'])['precio']:.2f} MXN")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()