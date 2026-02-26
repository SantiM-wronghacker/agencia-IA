"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza simulador crowdfunding inmobiliario
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

def calcular_interes(inversion, plazo, tasa):
    return inversion * (tasa / 100) * (plazo / 12)

def calcular_pago_mensual(inversion, plazo, tasa):
    return calcular_interes(inversion, plazo, tasa) / plazo

def calcular_pago_total(inversion, plazo, tasa):
    return inversion + calcular_interes(inversion, plazo, tasa)

def calcular_tasa_efectiva(tasa):
    return (1 + (tasa / 100)) ** (1 / 12) - 1

def main():
    try:
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        plazo = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        tasa = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0

        if plazo <= 0:
            raise ValueError("El plazo debe ser mayor que cero")
        if tasa < 0:
            raise ValueError("La tasa de interés no puede ser negativa")
        if inversion <= 0:
            raise ValueError("La inversión debe ser mayor que cero")

        interes = calcular_interes(inversion, plazo, tasa)
        pago_mensual = calcular_pago_mensual(inversion, plazo, tasa)
        pago_total = calcular_pago_total(inversion, plazo, tasa)
        tasa_efectiva = calcular_tasa_efectiva(tasa)

        print(f"Inversión: ${inversion:,.2f} MXN")
        print(f"Plazo: {plazo} meses")
        print(f"Tasa de interés: {tasa}%")
        print(f"Interés total: ${interes:,.2f} MXN")
        print(f"Pago mensual: ${pago_mensual:,.2f} MXN")
        print(f"Pago total: ${pago_total:,.2f} MXN")
        print(f"Tasa efectiva anual: {tasa_efectiva * 100:.2f}%")
        print(f"Fecha de inicio: {datetime.date.today()}")
        print(f"Fecha de vencimiento: {datetime.date.today() + datetime.timedelta(days=plazo*30)}")

        print("\nResumen Ejecutivo:")
        print(f"La inversión de ${inversion:,.2f} MXN durante {plazo} meses con una tasa de interés de {tasa}% generará un interés total de ${interes:,.2f} MXN y un pago mensual de ${pago_mensual:,.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()