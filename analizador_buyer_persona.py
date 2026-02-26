"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador buyer persona
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def calcular_edad(fecha_nacimiento):
    hoy = datetime.date.today()
    edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
    return edad

def analizar_buyer_persona(nombre, fecha_nacimiento, sexo, ingreso, gastos):
    edad = calcular_edad(fecha_nacimiento)
    categoria_edad = ""
    if edad < 25:
        categoria_edad = "Joven"
    elif edad < 45:
        categoria_edad = "Adulto"
    else:
        categoria_edad = "Adulto mayor"

    categoria_ingreso = ""
    if ingreso < 15000:
        categoria_ingreso = "Bajo"
    elif ingreso < 30000:
        categoria_ingreso = "Medio"
    else:
        categoria_ingreso = "Alto"

    categoria_gastos = ""
    if gastos < 5000:
        categoria_gastos = "Bajo"
    elif gastos < 10000:
        categoria_gastos = "Medio"
    else:
        categoria_gastos = "Alto"

    return {
        "nombre": nombre,
        "edad": edad,
        "categoria_edad": categoria_edad,
        "sexo": sexo,
        "ingreso": ingreso,
        "categoria_ingreso": categoria_ingreso,
        "gastos": gastos,
        "categoria_gastos": categoria_gastos
    }

def main():
    try:
        nombre = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        fecha_nacimiento = datetime.date(1995, 1, 1) if len(sys.argv) < 3 else datetime.datetime.strptime(sys.argv[2], "%Y-%m-%d").date()
        sexo = sys.argv[3] if len(sys.argv) > 3 else "Masculino"
        ingreso = int(sys.argv[4]) if len(sys.argv) > 4 else 25000
        gastos = int(sys.argv[5]) if len(sys.argv) > 5 else 8000

        buyer_persona = analizar_buyer_persona(nombre, fecha_nacimiento, sexo, ingreso, gastos)

        print(f"Nombre: {buyer_persona['nombre']}")
        print(f"Edad: {buyer_persona['edad']}")
        print(f"Categoría de edad: {buyer_persona['categoria_edad']}")
        print(f"Sexo: {buyer_persona['sexo']}")
        print(f"Ingreso mensual: ${buyer_persona['ingreso']:.2f} MXN")
        print(f"Categoría de ingreso: {buyer_persona['categoria_ingreso']}")
        print(f"Gastos mensuales: ${buyer_persona['gastos']:.2f} MXN")
        print(f"Categoría de gastos: {buyer_persona['categoria_gastos']}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()