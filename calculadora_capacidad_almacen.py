"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora capacidad almacen
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_capacidad_almacen(ancho, largo, alto, capacidad_contenedores):
    area_almacen = ancho * largo
    volumen_almacen = area_almacen * alto
    capacidad_total = volumen_almacen * capacidad_contenedores
    return capacidad_total

def calcular_peso_maximo(capacidad_total, densidad_contenido):
    peso_maximo = capacidad_total * densidad_contenido
    return peso_maximo

def main():
    try:
        ancho = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
        largo = float(sys.argv[2]) if len(sys.argv) > 2 else 20.0
        alto = float(sys.argv[3]) if len(sys.argv) > 3 else 5.0
        capacidad_contenedores = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        densidad_contenido = float(sys.argv[5]) if len(sys.argv) > 5 else 0.8

        capacidad_almacen = calcular_capacidad_almacen(ancho, largo, alto, capacidad_contenedores)
        peso_maximo = calcular_peso_maximo(capacidad_almacen, densidad_contenido)

        print(f"Ancho del almacén: {ancho} metros")
        print(f"Largo del almacén: {largo} metros")
        print(f"Alto del almacén: {alto} metros")
        print(f"Capacidad de los contenedores: {capacidad_contenedores} metros cúbicos")
        print(f"Densidad del contenido: {densidad_contenido} toneladas/metro cúbico")
        print(f"Capacidad total del almacén: {capacidad_almacen} metros cúbicos")
        print(f"Peso máximo que puede soportar el almacén: {peso_maximo} toneladas")
        print(f"Volumen del almacén: {ancho * largo * alto} metros cúbicos")
        print(f"Área del almacén: {ancho * largo} metros cuadrados")
        print(f"Perímetro del almacén: {2 * (ancho + largo)} metros")

        print("\nResumen Ejecutivo:")
        print(f"El almacén tiene una capacidad total de {capacidad_almacen} metros cúbicos y puede soportar un peso máximo de {peso_maximo} toneladas.")
        print(f"El almacén tiene un volumen de {ancho * largo * alto} metros cúbicos y un área de {ancho * largo} metros cuadrados.")

    except IndexError:
        print("Error: No se han proporcionado suficientes argumentos.")
    except ValueError:
        print("Error: Los argumentos proporcionados no son válidos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()