"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora liquidacion laboral
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime

def calcular_liquidacion(salario_diario, dias_trabajados, dias_vacaciones, prima_vacacional, aguinaldo, dias_aguinaldo):
    """
    Calcula la liquidación laboral según la legislación mexicana.
    """
    # Cálculo de salario ordinario
    salario_ordinario = salario_diario * dias_trabajados

    # Cálculo de vacaciones
    vacaciones = salario_diario * dias_vacaciones * (1 + prima_vacacional / 100)

    # Cálculo de aguinaldo
    aguinaldo_total = salario_diario * dias_aguinaldo

    # Cálculo de prima de antigüedad (12 días por año trabajado, máximo 2 años)
    años_trabajados = dias_trabajados / 365
    prima_antiguedad = min(2, años_trabajados) * 12 * salario_diario

    # Cálculo total
    total = salario_ordinario + vacaciones + aguinaldo_total + prima_antiguedad

    return {
        "salario_ordinario": salario_ordinario,
        "vacaciones": vacaciones,
        "aguinaldo": aguinaldo_total,
        "prima_antiguedad": prima_antiguedad,
        "total": total
    }

def main():
    try:
        # Parámetros por defecto realistas para México
        salario_diario = float(sys.argv[1]) if len(sys.argv) > 1 else 300.0
        dias_trabajados = int(sys.argv[2]) if len(sys.argv) > 2 else 180
        dias_vacaciones = int(sys.argv[3]) if len(sys.argv) > 3 else 6
        prima_vacacional = float(sys.argv[4]) if len(sys.argv) > 4 else 25.0
        dias_aguinaldo = int(sys.argv[5]) if len(sys.argv) > 5 else 15

        resultado = calcular_liquidacion(
            salario_diario, dias_trabajados, dias_vacaciones,
            prima_vacacional, dias_aguinaldo
        )

        print("Cálculo de liquidación laboral:")
        print(f"Salario ordinario: ${resultado['salario_ordinario']:,.2f}")
        print(f"Vacaciones: ${resultado['vacaciones']:,.2f}")
        print(f"Aguinaldo: ${resultado['aguinaldo']:,.2f}")
        print(f"Prima de antigüedad: ${resultado['prima_antiguedad']:,.2f}")
        print(f"Total a pagar: ${resultado['total']:,.2f}")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_liquidacion_laboral.py [salario_diario] [dias_trabajados] [dias_vacaciones] [prima_vacacional] [dias_aguinaldo]")
        print("Valores por defecto: 300.0 180 6 25.0 15")

if __name__ == "__main__":
    main()