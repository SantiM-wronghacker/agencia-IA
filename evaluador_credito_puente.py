"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza evaluador credito puente
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

def calcular_credito_puente(monto, plazo, tasa_interes):
    cuota = monto * (tasa_interes / 100) * (1 + tasa_interes / 100) ** plazo / ((1 + tasa_interes / 100) ** plazo - 1)
    return cuota

def calcular_interes_total(cuota, plazo):
    return cuota * plazo

def calcular_pago_total(monto, interes_total):
    return monto + interes_total

def calcular_tasa_mensual(tasa_anual):
    return tasa_anual / 12

def main():
    try:
        monto = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        plazo = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 15.0
        
        if monto <= 0:
            raise ValueError("El monto del crédito debe ser mayor a cero")
        if plazo <= 0:
            raise ValueError("El plazo del crédito debe ser mayor a cero")
        if tasa_interes <= 0:
            raise ValueError("La tasa de interés debe ser mayor a cero")
        
        cuota = calcular_credito_puente(monto, plazo, tasa_interes)
        interes_total = calcular_interes_total(cuota, plazo) - monto
        pago_total = calcular_pago_total(monto, interes_total)
        tasa_mensual = calcular_tasa_mensual(tasa_interes)
        
        print(f"Monto del crédito: ${monto:,.2f} MXN")
        print(f"Plazo del crédito: {plazo} meses")
        print(f"Tasa de interés anual: {tasa_interes}%")
        print(f"Tasa de interés mensual: {tasa_mensual:.2f}%")
        print(f"Cuota mensual: ${cuota:,.2f} MXN")
        print(f"Interés total: ${interes_total:,.2f} MXN")
        print(f"Pago total: ${pago_total:,.2f} MXN")
        print(f"Fecha de inicio: {datetime.date.today()}")
        print(f"Fecha de vencimiento: {(datetime.date.today() + datetime.timedelta(days=plazo*30)).strftime('%Y-%m-%d')}")
        
        print("\nResumen ejecutivo:")
        print(f"El crédito puente de ${monto:,.2f} MXN durante {plazo} meses con una tasa de interés anual de {tasa_interes}% tiene una cuota mensual de ${cuota:,.2f} MXN.")
        print(f"El pago total será de ${pago_total:,.2f} MXN, con un interés total de ${interes_total:,.2f} MXN.")
        
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()