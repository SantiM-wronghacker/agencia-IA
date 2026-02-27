# FINANZAS / Calculadora de tasa efectiva anual / Python

import sys
import math

def calcula_tasa_efectiva_anual(tasa_nominal, frecuencia):
    return (1 + (tasa_nominal / 100) / frecuencia) ** frecuencia - 1

def main():
    try:
        tasa_nominal = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
        frecuencia = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        tasa_efectiva_anual = calcula_tasa_efectiva_anual(tasa_nominal, frecuencia)
        print(f"Tasa nominal: {tasa_nominal}%")
        print(f"Frecuencia de pago: {frecuencia} veces al año")
        print(f"Tasa efectiva anual: {tasa_efectiva_anual * 100:.2f}%")
        print(f"Interés anual: {(tasa_efectiva_anual * 100):.2f}%")
        print(f"Ejemplo con $10,000: ${10000 * (1 + tasa_efectiva_anual):.2f}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()