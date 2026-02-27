# FINANZAS/ANALIZADOR DE PORTAFOLIO DE ACCIONES/PYTHON

import sys
import json
import datetime
import math
import random

def calcular_rendimiento(inversion, plazo):
    return inversion * math.pow(1 + 0.05, plazo)

def calcular_riesgo(inversion, plazo):
    return random.uniform(0, 1) * inversion * math.pow(1 + 0.05, plazo)

def main():
    try:
        args = sys.argv
        if len(args) < 3:
            inversion = 100000
            plazo = 5
        else:
            inversion = float(args[1])
            plazo = int(args[2])

        rendimiento = calcular_rendimiento(inversion, plazo)
        riesgo = calcular_riesgo(inversion, plazo)
        fecha_actual = datetime.datetime.now()
        fecha_vencimiento = fecha_actual + datetime.timedelta(days=plazo*365)

        print(f"Inversión inicial: ${inversion:.2f} MXN")
        print(f"Plazo de inversión: {plazo} años")
        print(f"Rendimiento esperado: ${rendimiento:.2f} MXN")
        print(f"Riesgo asociado: ${riesgo:.2f} MXN")
        print(f"Fecha de vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()