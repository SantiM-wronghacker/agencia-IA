# REAL ESTATE
# Analizador de plusvalia de colonia
# Python

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parametros default
        colonia = sys.argv[1] if len(sys.argv) > 1 else 'Polanco'
        precio_m2 = float(sys.argv[2]) if len(sys.argv) > 2 else 80000.0
        area = float(sys.argv[3]) if len(sys.argv) > 3 else 200.0
        incremento_anual = float(sys.argv[4]) if len(sys.argv) > 4 else 5.0
        anos = int(sys.argv[5]) if len(sys.argv) > 5 else 5
        tasa_inflacion = float(sys.argv[6]) if len(sys.argv) > 6 else 3.5

        # Calculo de plusvalia
        precio_inicial = precio_m2 * area
        plusvalia_anual = (precio_inicial * incremento_anual) / 100
        plusvalia_total = 0
        valor_actual = precio_inicial
        resultados_anuales = []
        for i in range(anos):
            plusvalia_anual = (valor_actual * incremento_anual) / 100
            valor_actual += plusvalia_anual
            valor_actual *= (1 + tasa_inflacion / 100)
            plusvalia_total += plusvalia_anual
            resultados_anuales.append({
                'año': i + 1,
                'plusvalia_anual': plusvalia_anual,
                'valor_actual': valor_actual
            })

        # Impresion de resultados
        print(f'Colonia: {colonia}')
        print(f'Precio inicial: ${precio_m2:.2f} por m2')
        print(f'Area: {area:.2f} m2')
        print(f'Plusvalia anual: {incremento_anual:.2f}%')
        print(f'Tasa de inflacion: {tasa_inflacion:.2f}%')
        print(f'Plusvalia total en {anos} anos: ${plusvalia_total:.2f}')
        print('Resultados anuales:')
        for resultado in resultados_anuales:
            print(f'Año {resultado["año"]}:')
            print(f'  Plusvalia anual: ${resultado["plusvalia_anual"]:.2f}')
            print(f'  Valor actual: ${resultado["valor_actual"]:.2f}')
            print(f'  Rentabilidad anual: {(resultado["plusvalia_anual"] / (resultado["valor_actual"] - resultado["plusvalia_anual"])) * 100:.2f}%')
        print('Resumen ejecutivo:')
        print(f'La plusvalia total en {anos} anos es de ${plusvalia_total:.2f}, lo que representa una rentabilidad del {(plusvalia_total / precio_inicial) * 100:.2f}%')
        print(f'El valor actual de la propiedad es de ${valor_actual:.2f}, lo que representa un incremento del {(valor_actual / precio_inicial) * 100:.2f}% con respecto al precio inicial')
        print(f'La tasa de crecimiento anual promedio es del {(incremento_anual + tasa_inflacion):.2f}%')
    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == "__main__":
    main()