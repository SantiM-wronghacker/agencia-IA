"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza conversor formatos datos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Conversión de temperatura
        temperatura_celsius = float(sys.argv[1]) if len(sys.argv) > 1 else 25
        temperatura_fahrenheit = temperatura_celsius * 9/5 + 32
        temperatura_kelvin = temperatura_celsius + 273.15
        print(f"Temperatura en Celsius: {temperatura_celsius}°C")
        print(f"Temperatura en Fahrenheit: {temperatura_fahrenheit}°F")
        print(f"Temperatura en Kelvin: {temperatura_kelvin} K")

        # Conversión de moneda
        cantidad_pesos = float(sys.argv[2]) if len(sys.argv) > 2 else 1000
        tipo_cambio = 20.5
        cantidad_dolares = cantidad_pesos / tipo_cambio
        cantidad_euros = cantidad_pesos / 24.5
        print(f"Cantidad en Pesos Mexicanos: ${cantidad_pesos} MXN")
        print(f"Cantidad en Dólares Americanos: ${cantidad_dolares:.2f} USD")
        print(f"Cantidad en Euros: ${cantidad_euros:.2f} EUR")

        # Conversión de fecha
        fecha_actual = datetime.datetime.now()
        fecha_formateada = fecha_actual.strftime("%d/%m/%Y %H:%M:%S")
        fecha_formateada_corta = fecha_actual.strftime("%d/%m/%Y")
        print(f"Fecha Actual: {fecha_formateada}")
        print(f"Fecha Actual (corta): {fecha_formateada_corta}")

        # Conversión de números
        numero_entero = int(sys.argv[3]) if len(sys.argv) > 3 else 12345
        numero_flotante = float(numero_entero)
        print(f"Número Entero: {numero_entero}")
        print(f"Número Flotante: {numero_flotante:.2f}")

        # Conversión de texto
        texto = sys.argv[4] if len(sys.argv) > 4 else "Hola, Mundo!"
        texto_mayusculas = texto.upper()
        texto_minusculas = texto.lower()
        print(f"Texto Original: {texto}")
        print(f"Texto en Mayúsculas: {texto_mayusculas}")
        print(f"Texto en Minúsculas: {texto_minusculas}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Temperatura en Celsius: {temperatura_celsius}°C")
        print(f"Cantidad en Pesos Mexicanos: ${cantidad_pesos} MXN")
        print(f"Fecha Actual: {fecha_formateada}")
        print(f"Número Entero: {numero_entero}")
        print(f"Texto Original: {texto}")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos")

if __name__ == "__main__":
    main()