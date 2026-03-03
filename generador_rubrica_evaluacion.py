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

def calcular_porcentaje(puntaje, puntaje_total):
    return (puntaje / puntaje_total) * 100

def calcular_promedio(puntajes):
    return sum(puntajes) / len(puntajes)

def calcular_max_y_min(puntajes):
    return max(puntajes), min(puntajes)

def calcular_estadisticas(rubrica):
    max_puntaje = max([p["puntaje"] for p in rubrica])
    min_puntaje = min([p["puntaje"] for p in rubrica])
    promedio_puntaje = calcular_promedio([p["puntaje"] for p in rubrica])
    return max_puntaje, min_puntaje, promedio_puntaje

def generar_rubrica(nivel_educativo, materia, numero_preguntas, puntaje_total):
    if numero_preguntas < 1:
        raise ValueError("Número de preguntas debe ser mayor que 0")
    if puntaje_total < 1:
        raise ValueError("Puntaje total debe ser mayor que 0")

    rubrica = []
    for i in range(numero_preguntas):
        pregunta = f"Pregunta {i+1}"
        puntaje = random.randint(1, 10)
        rubrica.append({"pregunta": pregunta, "puntaje": puntaje})

    return rubrica

def imprimir_resultados(nivel_educativo, materia, rubrica, max_puntaje, min_puntaje, promedio_puntaje):
    print(f"Nivel Educativo: {nivel_educativo}")
    print(f"Materia: {materia}")
    print(f"Número de Preguntas: {len(rubrica)}")
    print(f"Puntaje Total: {sum([p['puntaje'] for p in rubrica])}")
    print(f"Max Puntaje: {max_puntaje}")
    print(f"Min Puntaje: {min_puntaje}")
    print(f"Promedio Puntaje: {promedio_puntaje:.2f}%")
    print(f"Porcentaje de Aprobación: {calcular_porcentaje(sum([p['puntaje'] for p in rubrica]), sum([p['puntaje'] for p in rubrica])):.2f}%")
    print(f"Fecha de Generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duración de la Evaluación: {len(rubrica) * 5} minutos")

def imprimir_resumen_ejecutivo(nivel_educativo, materia, rubrica):
    print(f"Resumen Ejecutivo: Se generó una rubrica de {len(rubrica)} preguntas para el nivel de educación {nivel_educativo} y la materia {materia}.")
    print(f"Recomendaciones: Se sugiere revisar la rubrica antes de aplicarla a los estudiantes.")

def main():
    try:
        nivel_educativo = sys.argv[1]
        materia = sys.argv[2]
        numero_preguntas = int(sys.argv[3])
        puntaje_total = int(sys.argv[4])
    except IndexError:
        print("Error: Falta de parámetros")
        return

    try:
        rubrica = generar_rubrica(nivel_educativo, materia, numero_preguntas, puntaje_total)
        max_puntaje, min_puntaje, promedio_puntaje = calcular_estadisticas(rubrica)
        imprimir_resultados(nivel_educativo, materia, rubrica, max_puntaje, min_puntaje, promedio_puntaje)
        imprimir_resumen_ejecutivo(nivel_educativo, materia, rubrica)
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()