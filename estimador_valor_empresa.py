"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza estimador valor empresa
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
import random
from datetime import datetime

def estimador_valor_empresa(ingresos_anuales, gastos_anuales, activos, pasivos, tasa_interes, tasa_inflacion):
    try:
        utilidad_neta = ingresos_anuales - gastos_anuales
        valor_empresa = (utilidad_neta / (tasa_interes - tasa_inflacion)) + activos - pasivos
        if valor_empresa < 0:
            raise ValueError("El valor de la empresa no puede ser negativo")
        return valor_empresa
    except ZeroDivisionError:
        raise ValueError("La tasa de interés no puede ser igual a la tasa de inflación")

def calcular_tasa_interes(tipo_tasa):
    if tipo_tasa == "corta":
        return 0.05
    elif tipo_tasa == "larga":
        return 0.10
    else:
        raise ValueError("Tipo de tasa no válida")

def calcular_tasa_inflacion():
    return 0.03

def main():
    try:
        ingresos_anuales = float(sys.argv[1]) if len(sys.argv) > 1 else 10000000.0
        gastos_anuales = float(sys.argv[2]) if len(sys.argv) > 2 else 5000000.0
        activos = float(sys.argv[3]) if len(sys.argv) > 3 else 20000000.0
        pasivos = float(sys.argv[4]) if len(sys.argv) > 4 else 5000000.0
        tipo_tasa = sys.argv[5] if len(sys.argv) > 5 else "corta"

        tasa_interes = calcular_tasa_interes(tipo_tasa)
        tasa_inflacion = calcular_tasa_inflacion()

        valor_empresa = estimador_valor_empresa(ingresos_anuales, gastos_anuales, activos, pasivos, tasa_interes, tasa_inflacion)
        print(f"Valor de la empresa: {valor_empresa:.2f} MXN")
        print(f"Ingresos anuales: {ingresos_anuales:.2f} MXN")
        print(f"Gastos anuales: {gastos_anuales:.2f} MXN")
        print(f"Activos: {activos:.2f} MXN")
        print(f"Pasivos: {pasivos:.2f} MXN")
        print(f"Tasa de interés: {tasa_interes*100}%")
        print(f"Tasa de inflación: {tasa_inflacion*100}%")
        print(f"Fecha de estimación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Utilidad neta: {(ingresos_anuales - gastos_anuales):.2f} MXN")
        print(f"Resumen ejecutivo: La empresa tiene un valor de {valor_empresa:.2f} MXN, con ingresos anuales de {ingresos_anuales:.2f} MXN y gastos anuales de {gastos_anuales:.2f} MXN.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()