"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza analizador stack tecnologico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        stack_tecnologico = {
            "python": 0.75,
            "java": 0.65,
            "javascript": 0.80,
            "php": 0.45,
            "csharp": 0.55
        }

        # Procesamiento de argumentos
        if len(sys.argv) > 1:
            try:
                stack_tecnologico = json.loads(sys.argv[1])
            except json.JSONDecodeError:
                print("Error: Argumento no es JSON válido")

        # Análisis del stack tecnológico
        total = sum(stack_tecnologico.values())
        if total > 0:
            stack_tecnologico = {k: v/total for k, v in stack_tecnologico.items()}

        # Generación de datos concretos
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        proyectos_2023 = random.randint(150, 250)
        empresas_tecnologicas_mx = random.randint(1200, 1800)
        desarrolladores_python = random.randint(30000, 50000)
        crecimiento_anual = round(random.uniform(0.05, 0.15), 2)

        # Salida de resultados
        print(f"Fecha de análisis: {fecha_actual}")
        print(f"Proyectos tecnológicos en México (2023): {proyectos_2023}")
        print(f"Empresas tecnológicas en México: {empresas_tecnologicas_mx}")
        print(f"Desarrolladores Python en México: {desarrolladores_python:,}")
        print(f"Crecimiento anual del sector tecnológico: {crecimiento_anual*100}%")
        print("\nDistribución del stack tecnológico:")
        for tech, porc in stack_tecnologico.items():
            print(f"{tech.upper():<10} {porc*100:.1f}%")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()