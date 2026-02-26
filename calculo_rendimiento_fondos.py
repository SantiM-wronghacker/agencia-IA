"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo rendimiento fondos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

def calculo_rendimiento_fondos(inversion, tasa_interes, plazo):
    rendimiento = inversion * (1 + tasa_interes/100) ** plazo
    return rendimiento

def calculo_rendimiento_anual(rendimiento, inversion, plazo):
    return (rendimiento - inversion) / plazo

def calculo_tasa_inflacion(rendimiento, tasa_inflacion, plazo):
    return rendimiento / (1 + tasa_inflacion/100) ** plazo

def main():
    try:
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        tasa_interes = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        plazo = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        tasa_inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 3.0

        rendimiento = calculo_rendimiento_fondos(inversion, tasa_interes, plazo)
        rendimiento_anual = calculo_rendimiento_anual(rendimiento, inversion, plazo)
        rendimiento_real = calculo_tasa_inflacion(rendimiento, tasa_inflacion, plazo)

        print(f"Inversión inicial: ${inversion:.2f} MXN")
        print(f"Tasa de interés: {tasa_interes}%")
        print(f"Plazo: {plazo} años")
        print(f"Tasa de inflación: {tasa_inflacion}%")
        print(f"Rendimiento total: ${rendimiento:.2f} MXN")
        print(f"Rendimiento anual: ${rendimiento_anual:.2f} MXN")
        print(f"Rendimiento real (ajustado por inflación): ${rendimiento_real:.2f} MXN")
        print(f"Porcentaje de ganancia: {(rendimiento - inversion) / inversion * 100:.2f}%")
        print(f"Fecha de inicio: {datetime.date.today()}")
        print(f"Fecha de vencimiento: {(datetime.date.today() + datetime.timedelta(days=plazo*365))}")
        print("Resumen ejecutivo:")
        print(f"La inversión de ${inversion:.2f} MXN a una tasa de interés de {tasa_interes}% durante {plazo} años, con una tasa de inflación de {tasa_inflacion}%, generará un rendimiento total de ${rendimiento:.2f} MXN y un rendimiento anual de ${rendimiento_anual:.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()