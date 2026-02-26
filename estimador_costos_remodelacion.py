"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza estimador costos remodelacion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def calcular_costo_remodelacion(area_m2, tipo_remodelacion, calidad):
    """
    Calcula el costo estimado de remodelación en pesos mexicanos.
    """
    # Costos base por m2 (MXN)
    costos_base = {
        'baja': 1500,
        'media': 2500,
        'alta': 4000
    }

    # Ajuste por tipo de remodelación
    ajustes = {
        'cocina': 1.2,
        'baño': 1.1,
        'sala': 1.0,
        'recamara': 0.9,
        'integral': 1.3
    }

    # Ajuste por calidad
    calidad_factor = {
        'economica': 0.9,
        'estandar': 1.0,
        'premium': 1.2
    }

    costo_base = costos_base.get(tipo_remodelacion.lower(), 2500) * area_m2
    costo_ajustado = costo_base * ajustes.get(tipo_remodelacion.lower(), 1.0)
    costo_final = costo_ajustado * calidad_factor.get(calidad.lower(), 1.0)

    # Añadir variabilidad (+/- 10%)
    costo_final *= random.uniform(0.9, 1.1)

    return round(costo_final, 2)

def main():
    try:
        # Parámetros por defecto
        area_m2 = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
        tipo_remodelacion = sys.argv[2] if len(sys.argv) > 2 else 'media'
        calidad = sys.argv[3] if len(sys.argv) > 3 else 'estandar'

        costo = calcular_costo_remodelacion(area_m2, tipo_remodelacion, calidad)

        print("=== ESTIMADOR DE COSTOS DE REMODELACIÓN ===")
        print(f"Área: {area_m2:.2f} m²")
        print(f"Tipo de remodelación: {tipo_remodelacion}")
        print(f"Calidad: {calidad}")
        print(f"Costo estimado: ${costo:,.2f} MXN")
        print(f"Fecha de estimación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: python estimador_costos_remodelacion.py <area_m2> <tipo_remodelacion> <calidad>")
        print("Ejemplo: python estimador_costos_remodelacion.py 60 media estandar")

if __name__ == "__main__":
    main()