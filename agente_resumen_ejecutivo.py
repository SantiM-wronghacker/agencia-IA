"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza agente resumen ejecutivo
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Parámetros por defecto
        fecha_inicio = datetime.date.today() - datetime.timedelta(days=30)
        fecha_fin = datetime.date.today()
        num_registros = 10
        moneda = "MXN"
        tipo_cambio = 1.0

        # Parámetros de la línea de comandos
        if len(sys.argv) > 1:
            fecha_inicio = datetime.datetime.strptime(sys.argv[1], "%Y-%m-%d").date()
        if len(sys.argv) > 2:
            fecha_fin = datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        if len(sys.argv) > 3:
            num_registros = int(sys.argv[3])
        if len(sys.argv) > 4:
            moneda = sys.argv[4]
        if len(sys.argv) > 5:
            tipo_cambio = float(sys.argv[5])

        # Generar datos aleatorios
        registros = []
        total = 0.0
        max_valor = 0.0
        min_valor = float('inf')
        for _ in range(num_registros):
            fecha = fecha_inicio + datetime.timedelta(days=random.randint(0, (fecha_fin - fecha_inicio).days))
            valor = round(random.uniform(1000, 100000), 2)
            registros.append({"fecha": fecha.strftime("%Y-%m-%d"), "valor": valor})
            total += valor
            if valor > max_valor:
                max_valor = valor
            if valor < min_valor:
                min_valor = valor

        # Imprimir resumen ejecutivo
        print("Resumen Ejecutivo:")
        print(f"Fecha de inicio: {fecha_inicio}")
        print(f"Fecha de fin: {fecha_fin}")
        print(f"Numero de registros: {num_registros}")
        print(f"Moneda: {moneda}")
        print(f"Tipo de cambio: {tipo_cambio}")
        print("Registros:")
        for registro in registros:
            print(f"Fecha: {registro['fecha']}, Valor: {registro['valor']} {moneda}")
        print(f"Total: {total} {moneda}")
        print(f"Total con tipo de cambio: {total * tipo_cambio} USD")
        print(f"Maximo valor: {max_valor} {moneda}")
        print(f"Minimo valor: {min_valor} {moneda}")
        print(f"Promedio: {total / num_registros} {moneda}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo Final:")
        print(f"Total de registros procesados: {num_registros}")
        print(f"Total de valor procesado: {total} {moneda}")
        print(f"Tipo de cambio aplicado: {tipo_cambio}")
        print(f"Moneda de los registros: {moneda}")

    except Exception as e:
        print(f"Error: {str(e)}")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except IndexError as e:
        print(f"Error de indice: {str(e)}")

if __name__ == "__main__":
    main()