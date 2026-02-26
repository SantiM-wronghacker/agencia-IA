"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza generador receta estandarizada
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        nombre_receta = sys.argv[1] if len(sys.argv) > 1 else "Ensalada César"
        porciones = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        costo_porcion = float(sys.argv[3]) if len(sys.argv) > 3 else 59.90

        # Generar datos de la receta
        ingredientes = [
            {"nombre": "Lechuga romana", "cantidad": f"{random.randint(100, 200)}g"},
            {"nombre": "Pollo a la parrilla", "cantidad": f"{random.randint(150, 250)}g"},
            {"nombre": "Croutons", "cantidad": f"{random.randint(30, 50)}g"},
            {"nombre": "Queso parmesano", "cantidad": f"{random.randint(10, 20)}g"},
            {"nombre": "Aderezo César", "cantidad": f"{random.randint(30, 50)}ml"}
        ]

        # Cálculos
        costo_total = costo_porcion * porciones
        tiempo_preparacion = random.randint(10, 20)
        fecha_creacion = datetime.now().strftime("%Y-%m-%d")

        # Generar receta estandarizada
        receta = {
            "nombre": nombre_receta,
            "porciones": porciones,
            "costo_por_porcion": f"${costo_porcion:.2f}",
            "costo_total": f"${costo_total:.2f}",
            "tiempo_preparacion": f"{tiempo_preparacion} minutos",
            "fecha_creacion": fecha_creacion,
            "ingredientes": ingredientes
        }

        # Imprimir resultados
        print("RECETA ESTANDARIZADA")
        print(f"Nombre: {receta['nombre']}")
        print(f"Porciones: {receta['porciones']} | Costo total: {receta['costo_total']}")
        print(f"Tiempo de preparación: {receta['tiempo_preparacion']}")
        print("Ingredientes principales:")
        for ingrediente in receta['ingredientes']:
            print(f"- {ingrediente['nombre']}: {ingrediente['cantidad']}")

    except Exception as e:
        print(f"Error al generar la receta: {str(e)}")

if __name__ == "__main__":
    main()