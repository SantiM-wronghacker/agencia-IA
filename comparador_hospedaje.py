"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza comparador hospedaje
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
        # Definir opciones por defecto
        ciudad = sys.argv[1] if len(sys.argv) > 1 else "Cancun"
        num_hoteles = int(sys.argv[2]) if len(sys.argv) > 2 else 5

        # Simular datos de hospedaje
        hoteles = [
            {"nombre": "Hyatt Zilara Cancun", "precio": 4500.0, "calificacion": 4.8},
            {"nombre": "Secrets The Vine Cancun", "precio": 3800.0, "calificacion": 4.7},
            {"nombre": "Moon Palace Cancun", "precio": 3200.0, "calificacion": 4.5},
            {"nombre": "Iberostar Cancun", "precio": 4000.0, "calificacion": 4.6},
            {"nombre": "The Grand Park Royal Cancun", "precio": 3500.0, "calificacion": 4.4},
            {"nombre": "Fiesta Americana Grand Coral Beach", "precio": 4200.0, "calificacion": 4.5},
            {"nombre": "The Westin Lagunamar Ocean Resort Villas", "precio": 3000.0, "calificacion": 4.3},
            {"nombre": "Riu Cancun", "precio": 2800.0, "calificacion": 4.2},
            {"nombre": "Barcelo Maya Palace", "precio": 2500.0, "calificacion": 4.1},
            {"nombre": "Occidental at Xcaret Destination", "precio": 2200.0, "calificacion": 4.0},
        ]

        # Seleccionar los mejores hoteles
        mejores_hoteles = sorted(hoteles, key=lambda x: x["calificacion"], reverse=True)[:num_hoteles]

        # Imprimir resultados
        print(f"Comparación de hospedaje en {ciudad}:")
        print("-----------------------------------------")
        for i, hotel in enumerate(mejores_hoteles):
            print(f"{i+1}. {hotel['nombre']}: ${hotel['precio']:.2f} MXN, Calificación: {hotel['calificacion']:.2f}")
        print("-----------------------------------------")
        print(f"Promedio de precios: ${sum(hotel['precio'] for hotel in mejores_hoteles) / len(mejores_hoteles):.2f} MXN")
        print(f"Promedio de calificaciones: {sum(hotel['calificacion'] for hotel in mejores_hoteles) / len(mejores_hoteles):.2f}")
        print(f"Rango de precios: ${min(hotel['precio'] for hotel in mejores_hoteles):.2f} MXN - ${max(hotel['precio'] for hotel in mejores_hoteles):.2f} MXN")
        print(f"Resumen Ejecutivo: Los {num_hoteles} mejores hoteles en {ciudad} tienen un promedio de precio de ${sum(hotel['precio'] for hotel in mejores_hoteles) / len(mejores_hoteles):.2f} MXN y un promedio de calificación de {sum(hotel['calificacion'] for hotel in mejores_hoteles) / len(mejores_hoteles):.2f}")

    except IndexError:
        print("Error: Debe proporcionar la ciudad y el número de hoteles como argumentos.")
    except ValueError:
        print("Error: El número de hoteles debe ser un número entero.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()