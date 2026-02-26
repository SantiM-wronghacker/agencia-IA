"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza calculadora ocupacion renta
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_ocupacion_renta(precio_alquiler, precio_venta, tasa_interes_anual, gastos_mensuales, impuestos_anuales, seguro_anual):
    tasa_interes_mensual = tasa_interes_anual / 12
    ocupacion_renta = (precio_alquiler / precio_venta) * 12
    ocupacion_renta_descontada = ocupacion_renta - (gastos_mensuales / precio_venta) * 12 - (impuestos_anuales / precio_venta) - (seguro_anual / precio_venta) / 12
    return ocupacion_renta, ocupacion_renta_descontada

def main():
    try:
        precio_alquiler = float(sys.argv[1]) if len(sys.argv) > 1 else 15000.0
        precio_venta = float(sys.argv[2]) if len(sys.argv) > 2 else 2000000.0
        tasa_interes_anual = float(sys.argv[3]) if len(sys.argv) > 3 else 8.0
        gastos_mensuales = float(sys.argv[4]) if len(sys.argv) > 4 else 5000.0
        impuestos_anuales = float(sys.argv[5]) if len(sys.argv) > 5 else 20000.0
        seguro_anual = float(sys.argv[6]) if len(sys.argv) > 6 else 10000.0

        ocupacion_renta, ocupacion_renta_descontada = calcular_ocupacion_renta(precio_alquiler, precio_venta, tasa_interes_anual, gastos_mensuales, impuestos_anuales, seguro_anual)

        print(f"Precio de alquiler: ${precio_alquiler:.2f} MXN")
        print(f"Precio de venta: ${precio_venta:.2f} MXN")
        print(f"Tasa de interés anual: {tasa_interes_anual:.2f}%")
        print(f"Gastos mensuales: ${gastos_mensuales:.2f} MXN")
        print(f"Impuestos anuales: ${impuestos_anuales:.2f} MXN")
        print(f"Seguro anual: ${seguro_anual:.2f} MXN")
        print(f"Ocupación renta: {ocupacion_renta * 100:.2f}%")
        print(f"Ocupación renta descontada: {ocupacion_renta_descontada * 100:.2f}%")
        print(f"Rentabilidad anual: {(precio_alquiler * 12 - gastos_mensuales * 12 - impuestos_anuales - seguro_anual) / precio_venta * 100:.2f}%")
        print(f"Tiempo de recuperación de la inversión: {precio_venta / (precio_alquiler - gastos_mensuales):.2f} meses")
        print("Resumen ejecutivo:")
        print(f"La ocupación renta es de {ocupacion_renta * 100:.2f}% y la ocupación renta descontada es de {ocupacion_renta_descontada * 100:.2f}%.")
        print(f"La rentabilidad anual es de {(precio_alquiler * 12 - gastos_mensuales * 12 - impuestos_anuales - seguro_anual) / precio_venta * 100:.2f}%.")
        print(f"El tiempo de recuperación de la inversión es de {precio_venta / (precio_alquiler - gastos_mensuales):.2f} meses.")

    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos.")
        print("Uso: python calculadora_ocupacion_renta.py <precio_alquiler> <precio_venta> <tasa_interes_anual> <gastos_mensuales> <impuestos_anuales> <seguro_anual>")
    except ValueError:
        print("Error: Los argumentos deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()