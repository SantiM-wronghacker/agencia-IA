"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador rubrica evaluacion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Configuración por defecto
        if len(sys.argv) > 1:
            nivel_educativo = sys.argv[1]
            materia = sys.argv[2]
            numero_preguntas = int(sys.argv[3])
            puntaje_total = int(sys.argv[4])
        else:
            nivel_educativo = "Secundaria"
            materia = "Matemáticas"
            numero_preguntas = 10
            puntaje_total = 100

        # Validar parámetros
        if numero_preguntas < 1:
            raise ValueError("Número de preguntas debe ser mayor que 0")
        if puntaje_total < 1:
            raise ValueError("Puntaje total debe ser mayor que 0")

        # Generar rubrica de evaluación
        rubrica = []
        for i in range(numero_preguntas):
            pregunta = f"Pregunta {i+1}"
            puntaje = random.randint(1, 10)
            rubrica.append({"pregunta": pregunta, "puntaje": puntaje})

        # Calcular puntaje total
        puntaje_total_calculado = sum([p["puntaje"] for p in rubrica])

        # Calcular porcentaje de cada pregunta
        porcentajes = []
        for pregunta in rubrica:
            porcentaje = (pregunta["puntaje"] / puntaje_total_calculado) * 100
            porcentajes.append({"pregunta": pregunta["pregunta"], "porcentaje": porcentaje})

        # Imprimir resultados
        print(f"Nivel Educativo: {nivel_educativo}")
        print(f"Materia: {materia}")
        print(f"Numero de Preguntas: {numero_preguntas}")
        print(f"Puntaje Total: {puntaje_total_calculado}")
        print("Rubrica de Evaluación:")
        for pregunta in rubrica:
            print(f"{pregunta['pregunta']}: {pregunta['puntaje']} puntos")
        print("Porcentaje de cada pregunta:")
        for porcentaje in porcentajes:
            print(f"{porcentaje['pregunta']}: {porcentaje['porcentaje']:.2f}%")
        print(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Resumen Ejecutivo:")
        print(f"Se ha generado una rubrica de evaluación para {nivel_educativo} con {numero_preguntas} preguntas y un puntaje total de {puntaje_total_calculado} puntos.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()