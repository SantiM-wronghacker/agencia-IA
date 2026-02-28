# FINANZAS/ANALIZADOR DE PORTAFOLIO DE ACCIONES/PYTHON
# AREA: FINANZAS
# DESCRIPCION: Agente que realiza analizador portafolio acciones
# TECNOLOGIA: PYTHON

import sys
import json
import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_rendimiento(inversion, plazo, tasa_interes):
    return inversion * math.pow(1 + tasa_interes, plazo)

def calcular_riesgo(inversion, plazo, tasa_riesgo):
    return random.uniform(0, 1) * inversion * math.pow(1 + tasa_riesgo, plazo)

def calcular_impuestos(rendimiento, tasa_impuesto):
    return rendimiento * tasa_impuesto

def calcular_inflacion(rendimiento, tasa_inflacion):
    return rendimiento / math.pow(1 + tasa_inflacion, 1)

def main():
    try:
        args = sys.argv
        if len(args) < 5:
            inversion = 100000
            plazo = 5
            tasa_interes = 0.05
            tasa_riesgo = 0.02
            tasa_impuesto = 0.10
            tasa_inflacion = 0.03
        else:
            inversion = float(args[1])
            plazo = int(args[2])
            tasa_interes = float(args[3])
            tasa_riesgo = float(args[4])
            tasa_impuesto = float(args[5])
            tasa_inflacion = float(args[6])

        rendimiento = calcular_rendimiento(inversion, plazo, tasa_interes)
        riesgo = calcular_riesgo(inversion, plazo, tasa_riesgo)
        impuestos = calcular_impuestos(rendimiento, tasa_impuesto)
        inflacion = calcular_inflacion(rendimiento, tasa_inflacion)
        fecha_actual = datetime.datetime.now()
        fecha_vencimiento = fecha_actual + datetime.timedelta(days=plazo*365)

        print(f"Inversión inicial: ${inversion:.2f} MXN")
        print(f"Plazo de inversión: {plazo} años")
        print(f"Tasa de interés: {tasa_interes*100:.2f}%")
        print(f"Tasa de riesgo: {tasa_riesgo*100:.2f}%")
        print(f"Tasa de impuesto: {tasa_impuesto*100:.2f}%")
        print(f"Tasa de inflación: {tasa_inflacion*100:.2f}%")
        print(f"Rendimiento esperado: ${rendimiento:.2f} MXN")
        print(f"Riesgo asociado: ${riesgo:.2f} MXN")
        print(f"Impuestos: ${impuestos:.2f} MXN")
        print(f"Inflación: ${inflacion:.2f} MXN")
        print(f"Fecha de vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')}")
        print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y')}")
        print("Resumen ejecutivo:")
        print(f"La inversión de ${inversion:.2f} MXN durante {plazo} años con una tasa de interés de {tasa_interes*100:.2f}% y una tasa de riesgo de {tasa_riesgo*100:.2f}% puede generar un rendimiento de ${rendimiento:.2f} MXN, pero también conlleva un riesgo de ${riesgo:.2f} MXN y un impuesto de ${impuestos:.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()