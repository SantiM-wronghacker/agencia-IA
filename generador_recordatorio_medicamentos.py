"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador recordatorio medicamentos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        medicamentos = ["Paracetamol", "Ibuprofeno", "Aspirina"]
        dosis = [2, 1, 1]
        frecuencia = [8, 12, 24]
        hora_actual = datetime.datetime.now().hour

        # Procesar argumentos de la línea de comandos
        if len(sys.argv) > 1:
            medicamentos = sys.argv[1].split(",")
            if len(sys.argv) > 2:
                dosis = [int(x) for x in sys.argv[2].split(",")]
                if len(sys.argv) > 3:
                    frecuencia = [int(x) for x in sys.argv[3].split(",")]

        # Validar argumentos
        if len(medicamentos) != len(dosis) or len(medicamentos) != len(frecuencia):
            print("Error: La cantidad de medicamentos, dosis y frecuencia deben ser iguales")
            return

        # Generar recordatorios
        print("Recordatorios de medicamentos:")
        for i in range(len(medicamentos)):
            proxima_dosis = hora_actual + frecuencia[i]
            if proxima_dosis > 24:
                proxima_dosis -= 24
            print(f"  - {medicamentos[i]}: {dosis[i]} tabletas cada {frecuencia[i]} horas. Próxima dosis: {proxima_dosis}:00 hrs")
            print(f"    * Dosis diarias recomendadas: {math.ceil(24 / frecuencia[i]) * dosis[i]} tabletas")
            print(f"    * Cantidad de tabletas necesarias para un día: {math.ceil(24 / frecuencia[i]) * dosis[i]} tabletas")
        print(f"Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"Hora actual: {datetime.datetime.now().strftime('%H:%M:%S')}")
        print(f"Total de medicamentos: {len(medicamentos)}")
        print(f"Total de dosis diarias: {sum(dosis)} tabletas")
        print(f"Total de tabletas necesarias para un día: {sum([math.ceil(24 / x) * y for x, y in zip(frecuencia, dosis)])} tabletas")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"  - Total de medicamentos: {len(medicamentos)}")
        print(f"  - Total de dosis diarias: {sum(dosis)} tabletas")
        print(f"  - Total de tabletas necesarias para un día: {sum([math.ceil(24 / x) * y for x, y in zip(frecuencia, dosis)])} tabletas")
        print(f"  - Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"  - Hora actual: {datetime.datetime.now().strftime('%H:%M:%S')}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()