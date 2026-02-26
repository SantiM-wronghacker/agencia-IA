"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza calculadora retorno desarrollo obra
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        # Parámetros por defecto
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 10000000.0  # Precio de venta del inmueble
        costo_construccion = float(sys.argv[2]) if len(sys.argv) > 2 else 8000000.0  # Costo de construcción
        costo_terreno = float(sys.argv[3]) if len(sys.argv) > 3 else 1000000.0  # Costo del terreno
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.08  # Tasa de interés anual
        plazo = int(sys.argv[5]) if len(sys.argv) > 5 else 2  # Plazo de la inversión en años

        # Cálculo del retorno de la inversión
        retorno_inversion = (precio_venta - (costo_construccion + costo_terreno)) / (costo_construccion + costo_terreno)
        retorno_inversion_anual = (1 + retorno_inversion) ** (1 / plazo) - 1

        # Cálculo del valor actual neto (VAN)
        van = precio_venta / (1 + tasa_interes) ** plazo - (costo_construccion + costo_terreno)

        # Cálculo de la tasa interna de retorno (TIR)
        tir = (precio_venta / (costo_construccion + costo_terreno)) ** (1 / plazo) - 1

        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Costo de construcción: ${costo_construccion:,.2f} MXN")
        print(f"Costo del terreno: ${costo_terreno:,.2f} MXN")
        print(f"Retorno de la inversión: {retorno_inversion * 100:.2f}%")
        print(f"Retorno de la inversión anual: {retorno_inversion_anual * 100:.2f}%")
        print(f"Valor actual neto (VAN): ${van:,.2f} MXN")
        print(f"Tasa interna de retorno (TIR): {tir * 100:.2f}%")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()