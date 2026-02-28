"""
AREA: CEREBRO
DESCRIPCION: Agente que realiza clasificador intencion usuario
TECNOLOGIA: Python estandar
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

def clasificar_intencion_usuario(texto, intenciones):
    texto = texto.lower()
    for intencion, palabras_clave in intenciones.items():
        for palabra in palabras_clave:
            if palabra in texto:
                return intencion

    return "desconocida"

def obtener_fecha_y_hora_actual():
    return datetime.datetime.now()

def obtener_numero_aleatorio(minimo, maximo):
    return random.randint(minimo, maximo)

def obtener_valor_de_pi():
    return math.pi

def obtener_version_de_python():
    return sys.version

def obtener_sistema_operativo():
    return os.name

def obtener_directorio_actual():
    return os.getcwd()

def main():
    try:
        if len(sys.argv) > 1:
            texto = sys.argv[1]
        else:
            texto = "¿Qué tal?"

        intenciones = {
            "saludo": ["hola", "buenos días", "buenas tardes"],
            "despedida": ["adiós", "hasta luego", "chau"],
            "pregunta": ["¿qué", "¿cómo", "¿dónde"]
        }

        intencion = clasificar_intencion_usuario(texto, intenciones)
        fecha_y_hora_actual = obtener_fecha_y_hora_actual()
        numero_aleatorio = obtener_numero_aleatorio(1, 100)
        valor_de_pi = obtener_valor_de_pi()
        version_de_python = obtener_version_de_python()
        sistema_operativo = obtener_sistema_operativo()
        directorio_actual = obtener_directorio_actual()

        print(f"Intención del usuario: {intencion}")
        print(f"Fecha y hora actual: {fecha_y_hora_actual}")
        print(f"Número aleatorio: {numero_aleatorio}")
        print(f"Valor de pi: {valor_de_pi}")
        print(f"Versión de Python: {version_de_python}")
        print(f"Sistema operativo: {sistema_operativo}")
        print(f"Directorio actual: {directorio_actual}")
        print(f"Path de ejecución: {os.path.dirname(os.path.abspath(__file__))}")
        print(f"Nombre del archivo: {__file__}")
        print(f"Nombre del proceso: {os.getpid()}")
        print("Resumen ejecutivo:")
        print(f"  - Intención del usuario: {intencion}")
        print(f"  - Fecha y hora actual: {fecha_y_hora_actual}")
        print(f"  - Número aleatorio: {numero_aleatorio}")
        print(f"  - Valor de pi: {valor_de_pi}")
        print(f"  - Versión de Python: {version_de_python}")
        print(f"  - Sistema operativo: {sistema_operativo}")
        print(f"  - Directorio actual: {directorio_actual}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()