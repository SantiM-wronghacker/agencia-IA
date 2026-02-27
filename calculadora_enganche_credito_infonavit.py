# REAL ESTATE / Calculadora de Enganche de Credito Infonavit / Python

import sys
import json
import math

def calcula_enganche(sueldo, antiguedad, precio_casa):
    enganche = 0
    if sueldo <= 10000:
        enganche = precio_casa * 0.1
    elif sueldo <= 20000:
        enganche = precio_casa * 0.12
    else:
        enganche = precio_casa * 0.15
    if antiguedad >= 5:
        enganche *= 0.9
    return enganche

def main():
    try:
        sueldo = float(sys.argv[1]) if len(sys.argv) > 1 else 15000
        antiguedad = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        precio_casa = float(sys.argv[3]) if len(sys.argv) > 3 else 500000
        enganche = calcula_enganche(sueldo, antiguedad, precio_casa)
        print(f"Sueldo: ${sueldo:.2f}")
        print(f"Antigüedad: {antiguedad} años")
        print(f"Precio de la casa: ${precio_casa:.2f}")
        print(f"Enganche: ${enganche:.2f}")
        print(f"Crédito Infonavit: ${precio_casa - enganche:.2f}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()