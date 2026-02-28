"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza analizador razones financieras
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_razones_financieras(ventas, costos, gastos, activos, pasivos):
    try:
        # Calcular razón de liquidez
        liquidez = activos / pasivos

        # Calcular razón de endeudamiento
        endeudamiento = pasivos / activos

        # Calcular margen de utilidad neta
        utilidad_neta = (ventas - costos - gastos) / ventas

        # Calcular retorno sobre la inversión (ROI)
        roi = (utilidad_neta * ventas) / activos

        return {
            "liquidez": liquidez,
            "endeudamiento": endeudamiento,
            "utilidad_neta": utilidad_neta,
            "roi": roi
        }
    except ZeroDivisionError:
        return {
            "error": "No se puede dividir por cero"
        }
    except Exception as e:
        return {
            "error": str(e)
        }

def main():
    try:
        # Parámetros por defecto
        ventas = 1000000
        costos = 600000
        gastos = 150000
        activos = 500000
        pasivos = 200000

        # Obtener parámetros de la línea de comandos
        if len(sys.argv) > 1:
            ventas = int(sys.argv[1])
        if len(sys.argv) > 2:
            costos = int(sys.argv[2])
        if len(sys.argv) > 3:
            gastos = int(sys.argv[3])
        if len(sys.argv) > 4:
            activos = int(sys.argv[4])
        if len(sys.argv) > 5:
            pasivos = int(sys.argv[5])

        # Calcular razones financieras
        razones_financieras = calcular_razones_financieras(ventas, costos, gastos, activos, pasivos)

        # Imprimir resultados
        print("Razones Financieras:")
        print(f"Liquidez: {razones_financieras.get('liquidez', 0):.2f}")
        print(f"Endeudamiento: {razones_financieras.get('endeudamiento', 0):.2f}")
        print(f"Utilidad Neta: {razones_financieras.get('utilidad_neta', 0):.2f}")
        print(f"ROI: {razones_financieras.get('roi', 0):.2f}")
        print(f"Margen de Utilidad Bruta: {(ventas - costos) / ventas:.2f}")
        print(f"Margen de Utilidad Operativa: {(ventas - costos - gastos) / ventas:.2f}")
        print(f"Resumen Ejecutivo: La empresa tiene una liquidez de {razones_financieras.get('liquidez', 0):.2f}, un endeudamiento de {razones_financieras.get('endeudamiento', 0):.2f}, una utilidad neta de {razones_financieras.get('utilidad_neta', 0):.2f} y un ROI de {razones_financieras.get('roi', 0):.2f}.")
        if 'error' in razones_financieras:
            print(f"Error: {razones_financieras['error']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()