"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador estrategia referidos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        num_referidos = int(sys.argv[1]) if len(sys.argv) > 1 else 100
        porcentaje_comision = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
        monto_promedio = float(sys.argv[3]) if len(sys.argv) > 3 else 500.0

        # Validar parámetros
        if num_referidos <= 0:
            raise ValueError("Número de referidos debe ser mayor que 0")
        if porcentaje_comision < 0 or porcentaje_comision > 100:
            raise ValueError("Porcentaje de comisión debe estar entre 0 y 100")
        if monto_promedio <= 0:
            raise ValueError("Monto promedio debe ser mayor que 0")

        # Generar estrategia de referidos
        estrategia = {
            "num_referidos": num_referidos,
            "porcentaje_comision": porcentaje_comision,
            "monto_promedio": monto_promedio,
            "comision_total": num_referidos * monto_promedio * (porcentaje_comision / 100),
            "fecha_inicio": datetime.datetime.now().strftime("%Y-%m-%d"),
            "fecha_fin": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d")
        }

        # Imprimir resultados
        print(f"Número de referidos: {estrategia['num_referidos']}")
        print(f"Porcentaje de comisión: {estrategia['porcentaje_comision']}%")
        print(f"Monto promedio por referido: ${estrategia['monto_promedio']:.2f} MXN")
        print(f"Comisión total: ${estrategia['comision_total']:.2f} MXN")
        print(f"Fecha de inicio: {estrategia['fecha_inicio']}")
        print(f"Fecha de fin: {estrategia['fecha_fin']}")
        print(f"Comisión diaria promedio: ${estrategia['comision_total'] / 30:.2f} MXN")
        print(f"Comisión semanal promedio: ${estrategia['comision_total'] / 4:.2f} MXN")
        print(f"Comisión mensual promedio: ${estrategia['comision_total']:.2f} MXN")
        print(f"Impuesto sobre la renta (ISR) estimado: ${estrategia['comision_total'] * 0.10:.2f} MXN")
        print(f"Total a pagar después de impuestos: ${estrategia['comision_total'] - (estrategia['comision_total'] * 0.10):.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La estrategia de referidos generada tiene un potencial de comisión total de ${estrategia['comision_total']:.2f} MXN.")
        print(f"El número de referidos objetivo es de {estrategia['num_referidos']} personas.")
        print(f"El monto promedio por referido es de ${estrategia['monto_promedio']:.2f} MXN.")
        print(f"La comisión diaria promedio es de ${estrategia['comision_total'] / 30:.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()