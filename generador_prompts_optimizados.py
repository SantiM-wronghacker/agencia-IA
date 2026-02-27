"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza generador prompts optimizados
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
        # Configuración de parámetros
        num_prompts = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        longitud_min = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        longitud_max = int(sys.argv[3]) if len(sys.argv) > 3 else 20

        # Validación de parámetros
        if num_prompts <= 0:
            raise ValueError("El número de prompts debe ser mayor que 0")
        if longitud_min <= 0:
            raise ValueError("La longitud mínima debe ser mayor que 0")
        if longitud_max <= 0:
            raise ValueError("La longitud máxima debe ser mayor que 0")
        if longitud_min > longitud_max:
            raise ValueError("La longitud mínima no puede ser mayor que la longitud máxima")

        # Generación de prompts
        prompts = []
        for _ in range(num_prompts):
            longitud = random.randint(longitud_min, longitud_max)
            prompt = ''
            for _ in range(longitud):
                prompt += chr(random.randint(97, 122))  # Letras minúsculas
            prompts.append(prompt)

        # Impresión de resultados
        print(f"Fecha y hora actual: {datetime.datetime.now()}")
        print(f"Número de prompts generados: {len(prompts)}")
        print(f"Longitud mínima de los prompts: {longitud_min}")
        print(f"Longitud máxima de los prompts: {longitud_max}")
        print(f"Prompts generados:")
        for i, prompt in enumerate(prompts):
            print(f"{i+1}. {prompt}")
        print(f"Longitud promedio de los prompts: {sum(len(prompt) for prompt in prompts) / len(prompts):.2f}")
        print(f"Longitud máxima de los prompts generados: {max(len(prompt) for prompt in prompts)}")
        print(f"Longitud mínima de los prompts generados: {min(len(prompt) for prompt in prompts)}")
        print(f"Resumen ejecutivo:")
        print(f"  - Número de prompts: {len(prompts)}")
        print(f"  - Longitud promedio: {sum(len(prompt) for prompt in prompts) / len(prompts):.2f}")
        print(f"  - Longitud máxima: {max(len(prompt) for prompt in prompts)}")
        print(f"  - Longitud mínima: {min(len(prompt) for prompt in prompts)}")
        print(f"  - Fecha y hora de generación: {datetime.datetime.now()}")
        if len(prompts) > 0:
            print(f"  - Primer prompt: {prompts[0]}")
            print(f"  - Último prompt: {prompts[-1]}")
        else:
            print(f"  - No se generaron prompts")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error desconocido: {e}")

if __name__ == "__main__":
    main()