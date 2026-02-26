"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza generador encuesta satisfaccion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        num_empleados = 150
        num_preguntas = 5
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Generar datos de encuesta
        preguntas = [
            "¿Cómo califica su satisfacción laboral?",
            "¿Qué tan bien se comunica con su supervisor?",
            "¿Qué tan equilibrada es su carga de trabajo?",
            "¿Qué tan satisfecho está con su salario?",
            "¿Qué tan probable es que recomiende esta empresa a otros?"
        ]

        resultados = []
        for i in range(num_empleados):
            empleado = {
                "id": i + 1,
                "fecha": fecha_actual,
                "respuestas": [random.randint(1, 5) for _ in range(num_preguntas)]
            }
            resultados.append(empleado)

        # Calcular estadísticas
        total_satisfaccion = sum(sum(empleado["respuestas"] for empleado in resultados)) / (num_empleados * num_preguntas)
        promedio_superior = sum(1 for empleado in resultados if empleado["respuestas"][1] >= 4) / num_empleados * 100

        # Generar salida
        print("Encuesta de Satisfacción Laboral - Agencia Santi")
        print(f"Fecha: {fecha_actual}")
        print(f"Total de empleados encuestados: {num_empleados}")
        print(f"Puntuación promedio general: {total_satisfaccion:.2f}/5")
        print(f"Porcentaje de empleados con comunicación superior a 4/5: {promedio_superior:.1f}%")
        print("Datos generados correctamente.")

        # Guardar en archivo JSON
        with open("encuesta_satisfaccion.json", "w") as f:
            json.dump(resultados, f, indent=2)

    except Exception as e:
        print(f"Error al generar la encuesta: {str(e)}")

if __name__ == "__main__":
    main()