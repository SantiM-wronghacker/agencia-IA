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

def main():
    try:
        # Definir opciones por defecto
        ciudad = sys.argv[1] if len(sys.argv) > 1 else "Cancun"
        num_hoteles = int(sys.argv[2]) if len(sys.argv) > 2 else 5

        # Simular datos de hospedaje
        hoteles = [
            {"nombre": "Hotel 1", "precio": 1500.0, "calificacion": 4.5},
            {"nombre": "Hotel 2", "precio": 2000.0, "calificacion": 4.8},
            {"nombre": "Hotel 3", "precio": 1200.0, "calificacion": 4.2},
            {"nombre": "Hotel 4", "precio": 2500.0, "calificacion": 4.9},
            {"nombre": "Hotel 5", "precio": 1800.0, "calificacion": 4.6},
            {"nombre": "Hotel 6", "precio": 2200.0, "calificacion": 4.7},
            {"nombre": "Hotel 7", "precio": 1000.0, "calificacion": 4.1},
            {"nombre": "Hotel 8", "precio": 2800.0, "calificacion": 4.95},
            {"nombre": "Hotel 9", "precio": 1600.0, "calificacion": 4.4},
            {"nombre": "Hotel 10", "precio": 3000.0, "calificacion": 4.99},
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

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()