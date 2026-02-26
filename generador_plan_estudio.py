"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador plan estudio
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def generar_plan_estudio(areas=None, niveles=None, horas_semanales=None):
    # Datos base para el plan de estudio
    if areas is None:
        areas = ["Matemáticas", "Ciencias", "Historia", "Lengua", "Artes"]
    if niveles is None:
        niveles = ["Básico", "Intermedio", "Avanzado"]
    if horas_semanales is None:
        horas_semanales = [10, 15, 20, 25, 30]

    # Generar datos aleatorios pero realistas
    try:
        area_principal = random.choice(areas)
        nivel = random.choice(niveles)
        horas = random.choice(horas_semanales)
        duracion_meses = random.randint(3, 12)
        costo_mensual = round(random.uniform(1500, 5000), 2)
        costo_total = round(costo_mensual * duracion_meses, 2)
    except Exception as e:
        print(f"Error al generar el plan de estudio: {str(e)}", file=sys.stderr)
        sys.exit(1)

    # Formatear la salida
    plan = {
        "Área de estudio": area_principal,
        "Nivel": nivel,
        "Horas semanales": f"{horas} horas",
        "Duración": f"{duracion_meses} meses",
        "Costo mensual": f"${costo_mensual:.2f} MXN",
        "Costo total": f"${costo_total:.2f} MXN",
        "Fecha de generación": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Detalles": {
            "Descripción del área": f"El área de {area_principal} es fundamental para el desarrollo de habilidades",
            "Objetivos del nivel": f"El nivel {nivel} busca desarrollar habilidades avanzadas en {area_principal}",
            "Requisitos": "No se requieren conocimientos previos",
            "Beneficios": "Mejora la comprensión y el análisis de la materia"
        }
    }

    return plan

def main():
    try:
        if len(sys.argv) > 1:
            areas = sys.argv[1].split(',')
            niveles = sys.argv[2].split(',')
            horas_semanales = [int(x) for x in sys.argv[3].split(',')]
            plan_estudio = generar_plan_estudio(areas, niveles, horas_semanales)
        else:
            plan_estudio = generar_plan_estudio()
        print(json.dumps(plan_estudio, indent=2, ensure_ascii=False))
        print("\nResumen Ejecutivo:")
        print(f"El plan de estudio generado es para el área de {plan_estudio['Área de estudio']} con un nivel de {plan_estudio['Nivel']}.")
        print(f"El plan tiene una duración de {plan_estudio['Duración']} y un costo total de {plan_estudio['Costo total']}.")
    except Exception as e:
        print(f"Error al generar el plan de estudio: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()