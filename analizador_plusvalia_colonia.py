# REAL ESTATE/Analizador de plusvalia de colonia/Python

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Parametros default
        colonia = sys.argv[1] if len(sys.argv) > 1 else 'Polanco'
        precio_m2 = float(sys.argv[2]) if len(sys.argv) > 2 else 80000.0
        area = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0
        incremento_anual = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
        anos = int(sys.argv[5]) if len(sys.argv) > 5 else 5

        # Calculo de plusvalia
        precio_inicial = precio_m2 * area
        plusvalia_anual = (precio_inicial * incremento_anual) / 100
        plusvalia_total = 0
        for i in range(anos):
            plusvalia_total += plusvalia_anual
            precio_inicial += plusvalia_anual

        # Impresion de resultados
        print(f'Colonia: {colonia}')
        print(f'Precio inicial: ${precio_m2:.2f} por m2')
        print(f'Area: {area:.2f} m2')
        print(f'Plusvalia anual: {incremento_anual:.2f}%')
        print(f'Plusvalia total en {anos} anos: ${plusvalia_total:.2f}')

    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()