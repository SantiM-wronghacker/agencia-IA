# RESTAURANTES/CALCULADORA ROTACION MESA/PYTHON

import sys
import json
import datetime
import math
import random

def main():
    try:
        num_mesas = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        num_clientes = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        tiempo_rotacion = int(sys.argv[3]) if len(sys.argv) > 3 else 60

        print("Calculadora de Rotación de Mesas")
        print("---------------------------")
        print(f"Número de mesas: {num_mesas}")
        print(f"Número de clientes: {num_clientes}")
        print(f"Tiempo de rotación (minutos): {tiempo_rotacion}")

        clientes_por_mesa = num_clientes / num_mesas
        print(f"Clientes por mesa: {math.ceil(clientes_por_mesa)}")

        rotaciones_por_hora = 60 / tiempo_rotacion
        print(f"Rotaciones por hora: {math.floor(rotaciones_por_hora)}")

        ingresos_por_rotacion = 200  # promedio de gasto por cliente en un restaurante mexicano
        print(f"Ingresos por rotación: ${ingresos_por_rotacion * num_clientes}")

        ingresos_por_hora = ingresos_por_rotacion * num_clientes * rotaciones_por_hora
        print(f"Ingresos por hora: ${math.floor(ingresos_por_hora)}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()