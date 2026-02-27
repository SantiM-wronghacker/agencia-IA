# FRANQUICIAS / Calculadora de Regalias Franquicia / Python
import sys
import json
import datetime
import math
import random

def calcular_regalias(ventas, porcentaje_regalia):
    return ventas * porcentaje_regalia / 100

def main():
    try:
        ventas = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        porcentaje_regalia = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        regalia = calcular_regalias(ventas, porcentaje_regalia)
        print(f"Fecha de calculo: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"Ventas: ${ventas:,.2f} MXN")
        print(f"Porcentaje de regalia: {porcentaje_regalia}%")
        print(f"Regalia: ${regalia:,.2f} MXN")
        print(f"Total a pagar: ${ventas - regalia:,.2f} MXN")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()