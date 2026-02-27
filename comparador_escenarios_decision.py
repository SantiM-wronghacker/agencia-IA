# CEREBRO/Comparador de Escenarios de Decision/Python

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Definir escenarios de decision
        escenarios = [
            {"nombre": "Escenario 1", "costo": 100000, "beneficio": 200000},
            {"nombre": "Escenario 2", "costo": 150000, "beneficio": 300000},
            {"nombre": "Escenario 3", "costo": 200000, "beneficio": 400000}
        ]

        # Definir criterios de decision
        criterios = ["costo", "beneficio"]

        # Comparar escenarios de decision
        for escenario in escenarios:
            print(f"Escenario: {escenario['nombre']}")
            for criterio in criterios:
                print(f"{criterio.capitalize()}: {escenario[criterio]}")
            print(f"Rentabilidad: {escenario['beneficio'] - escenario['costo']}")
            print(f"Margen de beneficio: {(escenario['beneficio'] - escenario['costo']) / escenario['beneficio'] * 100}%")
            print("")

        # Seleccionar el mejor escenario
        mejor_escenario = max(escenarios, key=lambda x: x['beneficio'] - x['costo'])
        print(f"Mejor escenario: {mejor_escenario['nombre']}")
        print(f"Costo: {mejor_escenario['costo']}")
        print(f"Beneficio: {mejor_escenario['beneficio']}")
        print(f"Rentabilidad: {mejor_escenario['beneficio'] - mejor_escenario['costo']}")
        print(f"Margen de beneficio: {(mejor_escenario['beneficio'] - mejor_escenario['costo']) / mejor_escenario['beneficio'] * 100}%")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()