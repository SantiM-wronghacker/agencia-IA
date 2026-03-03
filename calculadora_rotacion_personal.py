"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora rotacion personal
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime
import math

def calcular_rotacion_personal(meses_trabajadores, trabajadores_inicial, trabajadores_final, bajas):
    """
    Calcula la rotación de personal en un periodo dado.
    """
    try:
        rotacion = (bajas / ((trabajadores_inicial + trabajadores_final) / 2)) * 100
        return round(rotacion, 2)
    except ZeroDivisionError:
        return 0

def calcular_costo_rotacion(rotacion, trabajadores_inicial, trabajadores_final, bajas):
    """
    Calcula el costo de la rotación de personal.
    """
    try:
        costo_promedio_reemplazo = 5000  # costo promedio de reemplazo de un trabajador en México
        costo_rotacion = (bajas / ((trabajadores_inicial + trabajadores_final) / 2)) * 100 * costo_promedio_reemplazo
        return round(costo_rotacion, 2)
    except ZeroDivisionError:
        return 0

def calcular_tiempo_promedio_rotacion(trabajadores_inicial, trabajadores_final, bajas):
    """
    Calcula el tiempo promedio de rotación de personal.
    """
    try:
        tiempo_promedio = (trabajadores_inicial - trabajadores_final) / bajas
        return round(tiempo_promedio, 2)
    except ZeroDivisionError:
        return 0

def calcular_costo_capacitacion(bajas):
    """
    Calcula el costo de capacitación de nuevos trabajadores.
    """
    try:
        costo_capacitacion = bajas * 2000  # costo promedio de capacitación de un trabajador en México
        return round(costo_capacitacion, 2)
    except ZeroDivisionError:
        return 0

def main():
    try:
        # Configuración por defecto
        meses_trabajadores = 12
        trabajadores_inicial = 100
        trabajadores_final = 95
        bajas = 5

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                trabajadores_inicial = int(sys.argv[1])
                trabajadores_final = int(sys.argv[2])
                bajas = int(sys.argv[3])
            except (ValueError, IndexError):
                pass

        # Cálculo
        rotacion = calcular_rotacion_personal(meses_trabajadores, trabajadores_inicial, trabajadores_final, bajas)
        costo_rotacion = calcular_costo_rotacion(rotacion, trabajadores_inicial, trabajadores_final, bajas)
        tiempo_promedio = calcular_tiempo_promedio_rotacion(trabajadores_inicial, trabajadores_final, bajas)
        costo_capacitacion = calcular_costo_capacitacion(bajas)

        # Salida
        print(f"Rotación de personal: {rotacion}%")
        print(f"Costo de la rotación de personal: ${costo_rotacion}")
        print(f"Tiempo promedio de rotación de personal: {tiempo_promedio} meses")
        print(f"Costo de capacitación de nuevos trabajadores: ${costo_capacitacion}")
        print(f"Trabajadores iniciales: {trabajadores_inicial}")
        print(f"Trabajadores finales: {trabajadores_final}")
        print(f"Bajas: {bajas}")
        print(f"Meses trabajadores: {meses_trabajadores}")
        print("Resumen ejecutivo:")
        print(f"La rotación de personal es del {rotacion}%, lo que genera un costo de ${costo_rotacion} y un tiempo promedio de rotación de {tiempo_promedio} meses.")
        print(f"El costo de capacitación de nuevos trabajadores es de ${costo_capacitacion}.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()