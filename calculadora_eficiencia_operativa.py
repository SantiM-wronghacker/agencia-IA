"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora eficiencia operativa
TECNOLOGÍA: Python estándar
"""

import sys
import math
import random
from datetime import datetime

def calculadora_eficiencia_operativa(ventas, costos, personal):
    try:
        eficiencia = (ventas - costos) / ventas
        productividad = ventas / personal
        rentabilidad = (ventas - costos) / personal
        margen_de_utilidad = (ventas - costos) / ventas
        retorno_de_la_inversion = (ventas - costos) / costos
        return eficiencia, productividad, rentabilidad, margen_de_utilidad, retorno_de_la_inversion
    except ZeroDivisionError:
        return None, None, None, None, None

def main():
    try:
        ventas = int(sys.argv[1]) if len(sys.argv) > 1 else 1000000
        costos = int(sys.argv[2]) if len(sys.argv) > 2 else 500000
        personal = int(sys.argv[3]) if len(sys.argv) > 3 else 10

        eficiencia, productividad, rentabilidad, margen_de_utilidad, retorno_de_la_inversion = calculadora_eficiencia_operativa(ventas, costos, personal)

        if eficiencia is not None:
            print(f"Fecha y hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"Ventas: ${ventas:,.2f} MXN")
            print(f"Costos: ${costos:,.2f} MXN")
            print(f"Personal: {personal} personas")
            print(f"Eficiencia operativa: {eficiencia*100:.2f}%")
            print(f"Productividad: ${productividad:,.2f} MXN por persona")
            print(f"Rentabilidad: ${rentabilidad:,.2f} MXN por persona")
            print(f"Margen de utilidad: {margen_de_utilidad*100:.2f}%")
            print(f"Retorno de la inversión: {retorno_de_la_inversion*100:.2f}%")
            print(f"Resumen ejecutivo: La eficiencia operativa es de {eficiencia*100:.2f}%, con una productividad de ${productividad:,.2f} MXN por persona y una rentabilidad de ${rentabilidad:,.2f} MXN por persona.")
        else:
            print("Error al calcular la eficiencia operativa")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()