# REAL ESTATE / Calculadora cap rate inmueble / Python

import sys
import math

def calcula_cap_rate(precio_venta, ingresos_anuales, gastos_anuales):
    cap_rate = ((ingresos_anuales - gastos_anuales) / precio_venta) * 100
    return cap_rate

def main():
    try:
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 5000000.0
        ingresos_anuales = float(sys.argv[2]) if len(sys.argv) > 2 else 120000.0
        gastos_anuales = float(sys.argv[3]) if len(sys.argv) > 3 else 30000.0

        cap_rate = calcula_cap_rate(precio_venta, ingresos_anuales, gastos_anuales)

        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Ingresos anuales: ${ingresos_anuales:,.2f} MXN")
        print(f"Gastos anuales: ${gastos_anuales:,.2f} MXN")
        print(f"Cap Rate: {cap_rate:.2f}%")
        print(f"Rentabilidad anual: ${(ingresos_anuales - gastos_anuales):,.2f} MXN")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()