"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador temario curso
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def generar_temario_curso():
    temas_base = [
        "Introducción a la educación en México",
        "Metodologías de enseñanza",
        "Evaluación educativa",
        "Tecnologías en el aula",
        "Inclusión y diversidad"
    ]

    sub_temas = {
        "Introducción a la educación en México": [
            "Sistema educativo mexicano",
            "Marco curricular nacional",
            "Políticas educativas actuales"
        ],
        "Metodologías de enseñanza": [
            "Aprendizaje basado en proyectos",
            "Clase invertida",
            "Gamificación educativa"
        ],
        "Evaluación educativa": [
            "Rúbricas de evaluación",
            "Evaluación formativa",
            "Evaluación sumativa"
        ],
        "Tecnologías en el aula": [
            "Herramientas digitales",
            "Plataformas educativas",
            "Seguridad digital en el aula"
        ],
        "Inclusión y diversidad": [
            "Educación inclusiva",
            "Atención a la diversidad",
            "Educación intercultural"
        ]
    }

    duracion_semanas = random.randint(8, 16)
    costo_mxn = random.randint(2000, 5000)
    participantes = random.randint(15, 30)

    temario = {
        "fecha_generacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temas": temas_base,
        "sub_temas": sub_temas,
        "duracion_semanas": duracion_semanas,
        "costo_mxn": costo_mxn,
        "participantes": participantes
    }

    return temario

def main():
    try:
        temario = generar_temario_curso()
        print("=== TEMARIO DE CURSO GENERADO ===")
        print(f"Fecha de generación: {temario['fecha_generacion']}")
        print(f"Duración: {temario['duracion_semanas']} semanas")
        print(f"Costo: ${temario['costo_mxn']} MXN")
        print(f"Participantes: {temario['participantes']}")
        print(f"Temas principales: {', '.join(temario['temas'])}")
    except Exception as e:
        print(f"Error al generar temario: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()