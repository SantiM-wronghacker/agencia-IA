"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza generador finiquito laboral
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime, timedelta
import random

def calcular_finiquito(salario_diario, antiguedad_dias, dias_trabajados_mes, dias_aguinaldo, dias_vacaciones):
    # Cálculos básicos
    prima_vacacional = salario_diario * dias_vacaciones * 0.25
    aguinaldo = salario_diario * dias_aguinaldo
    salario_mes = salario_diario * dias_trabajados_mes
    indemnizacion = salario_diario * antiguedad_dias * 0.3333

    # Total a pagar
    total = salario_mes + prima_vacacional + aguinaldo + indemnizacion

    return {
        "salario_diario": salario_diario,
        "antiguedad_dias": antiguedad_dias,
        "dias_trabajados_mes": dias_trabajados_mes,
        "dias_aguinaldo": dias_aguinaldo,
        "dias_vacaciones": dias_vacaciones,
        "prima_vacacional": prima_vacacional,
        "aguinaldo": aguinaldo,
        "indemnizacion": indemnizacion,
        "total": total
    }

def main():
    try:
        # Parámetros por defecto realistas para México
        salario_diario = float(sys.argv[1]) if len(sys.argv) > 1 else 350.0
        antiguedad_dias = int(sys.argv[2]) if len(sys.argv) > 2 else 180
        dias_trabajados_mes = int(sys.argv[3]) if len(sys.argv) > 3 else 30
        dias_aguinaldo = int(sys.argv[4]) if len(sys.argv) > 4 else 15
        dias_vacaciones = int(sys.argv[5]) if len(sys.argv) > 5 else 6

        finiquito = calcular_finiquito(
            salario_diario,
            antiguedad_dias,
            dias_trabajados_mes,
            dias_aguinaldo,
            dias_vacaciones
        )

        print("Finiquito Laboral Generado:")
        print(f"Salario diario: ${finiquito['salario_diario']:.2f}")
        print(f"Antigüedad: {finiquito['antiguedad_dias']} días")
        print(f"Prima vacacional: ${finiquito['prima_vacacional']:.2f}")
        print(f"Aguinaldo: ${finiquito['aguinaldo']:.2f}")
        print(f"Total a pagar: ${finiquito['total']:.2f}")

    except Exception as e:
        print(f"Error al generar finiquito: {str(e)}")

if __name__ == "__main__":
    main()