"""
AREA: CEREBRO
DESCRIPCION: Agente que procesa órdenes y muestra resultados
TECNOLOGIA: Python, importlib, sys
"""

import importlib.util
import sys
import traceback
import time
import os
import json
import datetime
import math
import re
import random

def cargar_maestro_ceo(archivo="maestro_ceo.py"):
    try:
        spec = importlib.util.spec_from_file_location("maestro_ceo", archivo)
        maestro_ceo = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(maestro_ceo)
        return maestro_ceo
    except FileNotFoundError:
        print(f"No se encontró el archivo {archivo}")
        sys.exit(1)
    except Exception as e:
        print(f"Error al cargar el módulo maestro_ceo: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

def obtener_orden(argv):
    if len(argv) > 1:
        return argv[1]
    else:
        return "orden por defecto"

def enviar_orden(orden, maestro_ceo):
    try:
        if hasattr(maestro_ceo, "procesar_orden"):
            resultado = getattr(maestro_ceo, "procesar_orden")(orden)
            return resultado
        else:
            print("El módulo maestro_ceo no tiene la función procesar_orden")
            return None
    except Exception as e:
        print(f"Error al procesar la orden: {str(e)}")
        traceback.print_exc()
        return None

def mostrar_progreso(resultado):
    if resultado is not None:
        print(f"Resultado: {resultado}")
    else:
        print("Orden desconocida o error al procesar.")

def mostrar_detalle(resultado):
    if resultado is not None:
        print(f"Detalle del resultado: {json.dumps(resultado, indent=4)}")
    else:
        print("No hay detalles disponibles.")

def mostrar_estadisticas():
    print(f"Fecha y hora actual: {datetime.datetime.now()}")
    print(f"Tiempo de ejecución: {time.time()} segundos")

def resumen_ejecutivo(orden, resultado):
    print(f"Resumen ejecutivo:")
    print(f"Orden: {orden}")
    print(f"Resultado: {resultado}")
    print(f"Fecha y hora actual: {datetime.datetime.now()}")

def main():
    archivo_maestro_ceo = sys.argv[1] if len(sys.argv) > 1 else "maestro_ceo.py"
    maestro_ceo = cargar_maestro_ceo(archivo_maestro_ceo)
    orden = obtener_orden(sys.argv)
    print(f"Orden: {orden}")
    resultado = enviar_orden(orden, maestro_ceo)
    mostrar_progreso(resultado)
    mostrar_detalle(resultado)
    mostrar_estadisticas()
    resumen_ejecutivo(orden, resultado)

if __name__ == "__main__":
    main()