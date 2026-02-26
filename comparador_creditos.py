"""
ÁREA: FINANZAS
DESCRIPCIÓN: Compara hasta 3 opciones de crédito hipotecario o empresarial. Calcula CAT, pago mensual, costo total y determina cuál conviene más según el perfil del usuario.
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_pago_mensual(monto, tasa, plazo):
    return monto * (tasa / 100 / 12) / (1 - math.pow(1 + tasa / 100 / 12, -plazo * 12))

def calcular_costo_total(monto, tasa, plazo):
    return calcular_pago_mensual(monto, tasa, plazo) * plazo * 12

def main():
    try:
        if len(sys.argv) == 6:
            monto = float(sys.argv[1])
            tasa1 = float(sys.argv[2])
            tasa2 = float(sys.argv[3])
            tasa3 = float(sys.argv[4])
            plazo = int(sys.argv[5])
        else:
            monto = 2000000
            tasa1 = 9.5
            tasa2 = 10.2
            tasa3 = 11.0
            plazo = 20

        pago_mensual1 = calcular_pago_mensual(monto, tasa1, plazo)
        pago_mensual2 = calcular_pago_mensual(monto, tasa2, plazo)
        pago_mensual3 = calcular_pago_mensual(monto, tasa3, plazo)

        costo_total1 = calcular_costo_total(monto, tasa1, plazo)
        costo_total2 = calcular_costo_total(monto, tasa2, plazo)
        costo_total3 = calcular_costo_total(monto, tasa3, plazo)

        cat1 = (costo_total1 - monto) / monto * 100
        cat2 = (costo_total2 - monto) / monto * 100
        cat3 = (costo_total3 - monto) / monto * 100

        print(f"Opción 1: CAT {cat1:.2f}%, pago mensual {pago_mensual1:.2f}, costo total {costo_total1:.2f}")
        print(f"Opción 2: CAT {cat2:.2f}%, pago mensual {pago_mensual2:.2f}, costo total {costo_total2:.2f}")
        print(f"Opción 3: CAT {cat3:.2f}%, pago mensual {pago_mensual3:.2f}, costo total {costo_total3:.2f}")

        if cat1 < cat2 and cat1 < cat3:
            print("La opción 1 conviene más")
        elif cat2 < cat1 and cat2 < cat3:
            print("La opción 2 conviene más")
        else:
            print("La opción 3 conviene más")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()