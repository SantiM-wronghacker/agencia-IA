"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza analizador merma desperdicio
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        dia = sys.argv[1] if len(sys.argv) > 1 else "2023-10-15"
        restaurante = sys.argv[2] if len(sys.argv) > 2 else "Restaurante Santi"

        # Datos simulados de merma
        productos = {
            "Carne": {"cantidad": 12.5, "precio_kg": 180.00},
            "Pescado": {"cantidad": 8.2, "precio_kg": 220.00},
            "Verduras": {"cantidad": 15.3, "precio_kg": 35.00},
            "Pan": {"cantidad": 4.0, "precio_kg": 45.00},
            "Lácteos": {"cantidad": 3.7, "precio_kg": 60.00}
        }

        # Cálculo de merma
        total_merma = 0.0
        for producto, datos in productos.items():
            merma = datos["cantidad"] * datos["precio_kg"]
            total_merma += merma

        # Generar reporte
        print(f"Reporte de Merma para {restaurante} - Fecha: {dia}")
        print(f"1. Carne: {productos['Carne']['cantidad']} kg - Pérdida: ${productos['Carne']['cantidad'] * productos['Carne']['precio_kg']:.2f}")
        print(f"2. Pescado: {productos['Pescado']['cantidad']} kg - Pérdida: ${productos['Pescado']['cantidad'] * productos['Pescado']['precio_kg']:.2f}")
        print(f"3. Verduras: {productos['Verduras']['cantidad']} kg - Pérdida: ${productos['Verduras']['cantidad'] * productos['Verduras']['precio_kg']:.2f}")
        print(f"4. Pan: {productos['Pan']['cantidad']} kg - Pérdida: ${productos['Pan']['cantidad'] * productos['Pan']['precio_kg']:.2f}")
        print(f"5. Total de merma: ${total_merma:.2f}")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()