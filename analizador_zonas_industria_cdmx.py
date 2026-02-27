# BIENES RAICES COMERCIALES - ANALIZADOR ZONAS INDUSTRIA CDMX - PYTHON

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Configuracion por defecto
        zona_default = 'Cuauhtemoc'
        precio_default = 5000000
        area_default = 1000

        # Argumentos de linea de comando
        if len(sys.argv) > 1:
            zona = sys.argv[1]
        else:
            zona = zona_default

        if len(sys.argv) > 2:
            precio = int(sys.argv[2])
        else:
            precio = precio_default

        if len(sys.argv) > 3:
            area = int(sys.argv[3])
        else:
            area = area_default

        # Datos de zonas industriales en CDMX
        zonas_industriales = {
            'Cuauhtemoc': {'precio': 5000000, 'area': 1000},
            'Miguel Hidalgo': {'precio': 6000000, 'area': 1200},
            'Alvaro Obregon': {'precio': 5500000, 'area': 1100},
            'Benito Juarez': {'precio': 5800000, 'area': 1150},
            'Coyoacan': {'precio': 5200000, 'area': 1050},
        }

        # Analisis de zona industrial
        if zona in zonas_industriales:
            zona_industrial = zonas_industriales[zona]
            print(f"Zona industrial: {zona}")
            print(f"Precio por metro cuadrado: ${zona_industrial['precio'] / zona_industrial['area']:.2f}")
            print(f"Area total: {zona_industrial['area']} m2")
            print(f"Precio total: ${zona_industrial['precio']:.2f}")
            print(f"Numero de locales: {math.floor(zona_industrial['area'] / 100)}")
        else:
            print(f"Zona industrial no encontrada: {zona}")
            print(f"Precio por metro cuadrado: ${precio / area:.2f}")
            print(f"Area total: {area} m2")
            print(f"Precio total: ${precio:.2f}")
            print(f"Numero de locales: {math.floor(area / 100)}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()