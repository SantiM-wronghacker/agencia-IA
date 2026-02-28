"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza calculadora roi renta vacacional
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculadora_roi(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    roi = (renta_mensual - gastos_mensuales) * 12 / (precio_compra + gastos_iniciales)
    roi_anualizado = roi * (1 + tasa_interes/100)
    return roi_anualizado

def calculadora_roi_mensual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    roi_mensual = (renta_mensual - gastos_mensuales) / (precio_compra + gastos_iniciales)
    return roi_mensual

def calculadora_pago_anual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes):
    pago_anual = (renta_mensual - gastos_mensuales) * 12
    return pago_anual

def main():
    try:
        precio_compra = float(sys.argv[1]) if len(sys.argv) > 1 else 2000000.0
        gastos_iniciales = float(sys.argv[2]) if len(sys.argv) > 2 else 50000.0
        renta_mensual = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.0
        gastos_mensuales = float(sys.argv[4]) if len(sys.argv) > 4 else 3000.0
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 8.0

        roi_anualizado = calculadora_roi(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)
        roi_mensual = calculadora_roi_mensual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)
        pago_anual = calculadora_pago_anual(precio_compra, gastos_iniciales, renta_mensual, gastos_mensuales, tasa_interes)

        print("Precio de compra: $", precio_compra)
        print("Gastos iniciales: $", gastos_iniciales)
        print("Renta mensual: $", renta_mensual)
        print("Gastos mensuales: $", gastos_mensuales)
        print("Tasa de interés: {:.2f}%".format(tasa_interes))
        print("ROI anualizado: {:.2f}%".format(roi_anualizado*100))
        print("ROI mensual: {:.2f}%".format(roi_mensual*100))
        print("Pago anual: $", pago_anual)
        print("Resumen ejecutivo:")
        print("La inversión en renta vacacional tiene un ROI anualizado de {:.2f}% y un pago anual de ${:.2f}".format(roi_anualizado*100, pago_anual))

    except IndexError:
        print("Error: Falta de argumentos. Utilice el formato 'python calculadora_roi_renta_vacacional.py <precio_compra> <gastos_iniciales> <renta_mensual> <gastos_mensuales> <tasa_interes>'")
    except ValueError:
        print("Error: Valor no numérico. Utilice el formato 'python calculadora_roi_renta_vacacional.py <precio_compra> <gastos_iniciales> <renta_mensual> <gastos_mensuales> <tasa_interes>'")
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()