"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza analizador habitos saludables
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        peso = float(sys.argv[2]) if len(sys.argv) > 2 else 70.5
        altura = float(sys.argv[3]) if len(sys.argv) > 3 else 1.70
        pasos_diarios = int(sys.argv[4]) if len(sys.argv) > 4 else 5000
        horas_sueño = float(sys.argv[5]) if len(sys.argv) > 5 else 7.0

        # Cálculo de IMC
        imc = peso / (altura ** 2)
        categoria = "Normal" if 18.5 <= imc <= 24.9 else "Sobrepeso" if imc >= 25 else "Bajo peso"

        # Datos de referencia mexicanos
        promedio_pasos_mx = 4500
        promedio_sueno_mx = 6.5
        consumo_agua_recomendado = 2.5  # litros por día

        # Generar datos aleatorios para el análisis
        actividad_fisica = random.randint(1, 100)
        consumo_agua = random.uniform(1.0, 3.5)
        estres = random.randint(1, 10)

        # Generar fecha de análisis
        fecha_analisis = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Resultados
        print("=== ANÁLISIS DE HÁBITOS SALUDABLES ===")
        print(f"Fecha: {fecha_analisis}")
        print(f"IMC: {imc:.2f} ({categoria})")
        print(f"Pasos diarios: {pasos_diarios} (Promedio MX: {promedio_pasos_mx})")
        print(f"Horas de sueño: {horas_sueño} (Promedio MX: {promedio_sueno_mx})")
        print(f"Consumo de agua: {consumo_agua:.1f} litros (Recomendado: {consumo_agua_recomendado} litros)")
        print(f"Nivel de estrés: {estres}/10")
        print(f"Actividad física: {actividad_fisica}%")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()