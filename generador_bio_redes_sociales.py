"""
AREA: MARKETING
DESCRIPCION: Agente que realiza generador bio redes sociales
TECNOLOGIA: Python estandar
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
        if len(sys.argv) != 6:
            raise ValueError("Necesita proporcionar los siguientes argumentos: nombre_agencia, ciudad, num_clientes, num_proyectos, num_empleados")

        nombre_agencia = sys.argv[1]
        ciudad = sys.argv[2]
        num_clientes = int(sys.argv[3])
        num_proyectos = int(sys.argv[4])
        num_empleados = int(sys.argv[5])

        if num_clientes < 0 or num_proyectos < 0 or num_empleados < 0:
            raise ValueError("Los numeros de clientes, proyectos y empleados no pueden ser negativos")

        bio = f"Somos {nombre_agencia}, una agencia de marketing con sede en {ciudad}. Contamos con {num_clientes} clientes satisfechos y hemos realizado {num_proyectos} proyectos exitosos. Nuestro equipo está conformado por {num_empleados} empleados altamente capacitados."

        print("Bio Redes Sociales:")
        print("--------------------")
        print(bio)
        print(f"Número de clientes: {num_clientes}")
        print(f"Número de proyectos: {num_proyectos}")
        print(f"Número de empleados: {num_empleados}")
        print(f"Fecha actual: {datetime.date.today()}")
        print(f"Promedio de proyectos por empleado: {num_proyectos / num_empleados:.2f}")
        print(f"Promedio de clientes por proyecto: {num_clientes / num_proyectos:.2f}")

        datos = {
            "nombre_agencia": nombre_agencia,
            "ciudad": ciudad,
            "num_clientes": num_clientes,
            "num_proyectos": num_proyectos,
            "num_empleados": num_empleados,
            "fecha_actual": str(datetime.date.today()),
            "promedio_proyectos_por_empleado": num_proyectos / num_empleados,
            "promedio_clientes_por_proyecto": num_clientes / num_proyectos
        }

        print("\nDatos en formato JSON:")
        print("------------------------")
        print(json.dumps(datos, indent=4))

        print("\nResumen Ejecutivo:")
        print("--------------------")
        print(f"La agencia {nombre_agencia} tiene un total de {num_clientes} clientes y ha realizado {num_proyectos} proyectos con un equipo de {num_empleados} empleados. El promedio de proyectos por empleado es de {num_proyectos / num_empleados:.2f} y el promedio de clientes por proyecto es de {num_clientes / num_proyectos:.2f}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()