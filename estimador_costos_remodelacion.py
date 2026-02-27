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
        'baja': 1800,
        'media': 3000,
        'alta': 5000
    }

    # Ajuste por tipo de remodelación
    ajustes = {
        'cocina': 1.3,
        'baño': 1.2,
        'sala': 1.1,
        'recamara': 1.0,
        'integral': 1.4
    }

    # Ajuste por calidad
    calidad_factor = {
        'economica': 0.8,
        'estandar': 1.0,
        'premium': 1.3
    }

    costo_base = costos_base.get(calidad.lower(), 3000) * area_m2
    costo_ajustado = costo_base * ajustes.get(tipo_remodelacion.lower(), 1.0)
    costo_final = costo_ajustado * calidad_factor.get(calidad.lower(), 1.0)

    # Añadir variabilidad (+/- 10%)
    costo_final *= random.uniform(0.9, 1.1)

    return round(costo_final, 2)

def main():
    try:
        # Parámetros por defecto
        area_m2 = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
        tipo_remodelacion = sys.argv[2].lower() if len(sys.argv) > 2 else 'media'
        calidad = sys.argv[3].lower() if len(sys.argv) > 3 else 'estandar'

        if tipo_remodelacion not in ['cocina', 'baño', 'sala', 'recamara', 'integral']:
            raise ValueError("Tipo de remodelación no válido")

        if calidad not in ['economica', 'estandar', 'premium']:
            raise ValueError("Calidad no válida")

        costo = calcular_costo_remodelacion(area_m2, tipo_remodelacion, calidad)

        print("=== ESTIMADOR DE COSTOS DE REMODELACIÓN ===")
        print(f"Área: {area_m2:.2f} m²")
        print(f"Tipo de remodelación: {tipo_remodelacion.capitalize()}")
        print(f"Calidad: {calidad.capitalize()}")
        print(f"Costo estimado: ${costo:,.2f} MXN")
        print(f"Fecha de estimación: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=== RESUMEN EJECUTIVO ===")
        print(f"El costo estimado para remodelar {area_m2:.2f} m² de {tipo_remodelacion} con calidad {calidad} es de ${costo:,.2f} MXN.")

    except ValueError as e:
        print(f"Error: {str(e)}")
        print("Uso: python estimador_costos_remodelacion.py <area_m2> <tipo_remodelacion> <calidad>")
        print("Ejemplo: python estimador_costos_remodelacion.py 50 cocina estandar")
        print("Tipos de remodelación: cocina, baño, sala, recamara, integral")
        print("Calidades: economica, estandar, premium")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: python estimador_costos_remodelacion.py <area_m2> <tipo_remodelacion> <calidad>")
        print("Ejemplo: python estimador_costos_remodelacion.py 50 cocina estandar")