"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza analizador clima organizacional
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        empresa = "Agencia Santi"
        fecha = datetime.now().strftime("%Y-%m-%d")
        empleados = 150
        satisfaccion = random.uniform(75, 90)
        rotacion = random.uniform(5, 15)
        productividad = random.uniform(80, 95)

        # Generar datos de clima organizacional
        datos = {
            "empresa": empresa,
            "fecha": fecha,
            "empleados": empleados,
            "satisfaccion_promedio": round(satisfaccion, 2),
            "rotacion_anual": round(rotacion, 2),
            "productividad_promedio": round(productividad, 2),
            "indicadores": {
                "comunicacion": random.randint(70, 90),
                "liderazgo": random.randint(65, 85),
                "reconocimiento": random.randint(50, 75),
                "equilibrio": random.randint(60, 80),
                "crecimiento": random.randint(70, 90)
            }
        }

        # Imprimir resultados
        print(f"Análisis de clima organizacional para {empresa}")
        print(f"Fecha: {fecha}")
        print(f"Número de empleados: {empleados}")
        print(f"Satisfacción promedio: {datos['satisfaccion_promedio']}%")
        print(f"Rotación anual: {datos['rotacion_anual']}%")
        print(f"Productividad promedio: {datos['productividad_promedio']}%")
        print("\nIndicadores clave:")
        for key, value in datos['indicadores'].items():
            print(f"- {key.capitalize()}: {value}%")

        # Guardar en archivo JSON
        with open("clima_organizacional.json", "w") as f:
            json.dump(datos, f, indent=4)

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()