# RESTAURANTES/CALCULADORA ROTACION MESA/PYTHON

import sys
import json
import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        num_mesas = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        num_clientes = int(sys.argv[2]) if len(sys.argv) > 2 else 50
        tiempo_rotacion = int(sys.argv[3]) if len(sys.argv) > 3 else 60
        gasto_promedio = float(sys.argv[4]) if len(sys.argv) > 4 else 200.0
        horas_operacion = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        dias_operacion = int(sys.argv[6]) if len(sys.argv) > 6 else 7

        print("Calculadora de Rotación de Mesas")
        print("---------------------------")
        print(f"Número de mesas: {num_mesas}")
        print(f"Número de clientes: {num_clientes}")
        print(f"Tiempo de rotación (minutos): {tiempo_rotacion}")
        print(f"Gasto promedio por cliente: ${gasto_promedio}")
        print(f"Horas de operación: {horas_operacion}")
        print(f"Días de operación: {dias_operacion}")

        clientes_por_mesa = num_clientes / num_mesas
        print(f"Clientes por mesa: {math.ceil(clientes_por_mesa)}")

        rotaciones_por_hora = 60 / tiempo_rotacion
        print(f"Rotaciones por hora: {math.floor(rotaciones_por_hora)}")

        ingresos_por_rotacion = gasto_promedio * num_clientes
        print(f"Ingresos por rotación: ${math.floor(ingresos_por_rotacion)}")

        ingresos_por_hora = ingresos_por_rotacion * rotaciones_por_hora
        print(f"Ingresos por hora: ${math.floor(ingresos_por_hora)}")

        ingresos_por_dia = ingresos_por_hora * horas_operacion
        print(f"Ingresos por día: ${math.floor(ingresos_por_dia)}")

        ingresos_por_semana = ingresos_por_dia * dias_operacion
        print(f"Ingresos por semana: ${math.floor(ingresos_por_semana)}")

        ingresos_por_mes = ingresos_por_semana * 4
        print(f"Ingresos por mes: ${math.floor(ingresos_por_mes)}")

        print("\nResumen Ejecutivo:")
        print(f"Con {num_mesas} mesas y {num_clientes} clientes, el ingreso por hora es de ${math.floor(ingresos_por_hora)}.")
        print(f"El ingreso por día es de ${math.floor(ingresos_por_dia)}, lo que representa un ingreso por mes de ${math.floor(ingresos_por_mes)}.")
        print(f"El ingreso anual es de ${math.floor(ingresos_por_mes * 12)}.")
        print(f"El número de clientes atendidos por día es de {math.ceil(clientes_por_mesa * num_mesas * rotaciones_por_hora * horas_operacion)}.")
        print(f"El número de clientes atendidos por mes es de {math.ceil(clientes_por_mesa * num_mesas * rotaciones_por_hora * horas_operacion * dias_operacion * 4)}.")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()