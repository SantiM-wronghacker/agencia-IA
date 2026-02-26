"""
ÁREA: CEREBRO
DESCRIPCIÓN: Toma outputs de múltiples agentes y genera un reporte ejecutivo unificado en texto plano. Ideal para consolidar análisis del Clawbot en un documento enviable.
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import os

def calcular_rendimiento(inversion, plazo, tasa_interes):
    return inversion * (tasa_interes / 100) * (plazo / 12)

def calcular_rendimiento_anual(rendimiento_mensual):
    return rendimiento_mensual * 12

def calcular_beneficio_esperado(inversion, tasa_interes):
    return inversion * (tasa_interes / 100)

def main():
    try:
        if len(sys.argv) > 1:
            titulo = sys.argv[1]
            inversion = float(sys.argv[2])
            plazo = int(sys.argv[3])
            tasa_interes = float(sys.argv[4])
        else:
            titulo = 'Análisis Inversión Polanco'
            inversion = 100000.0
            plazo = 12
            tasa_interes = 15.0
        
        rendimiento_mensual = calcular_rendimiento(inversion, plazo, tasa_interes)
        rendimiento_anual = calcular_rendimiento_anual(rendimiento_mensual)
        beneficio_esperado = calcular_beneficio_esperado(inversion, tasa_interes)

        reporte = f"Reporte: {titulo}\n"
        reporte += f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d')}\n"
        reporte += "Resumen de Análisis:\n"
        reporte += f"  - Inversión Total: ${inversion:,.2f}\n"
        reporte += f"  - Beneficio Esperado: {tasa_interes}% (${beneficio_esperado:,.2f})\n"
        reporte += f"  - Plazo de Inversión: {plazo} meses\n"
        reporte += f"  - Rendimiento Anual: ${rendimiento_anual:,.2f}\n"
        reporte += f"  - Rendimiento Mensual: ${rendimiento_mensual:,.2f}\n"
        reporte += "\nResumen Ejecutivo:\n"
        reporte += f"La inversión de ${inversion:,.2f} durante {plazo} meses con una tasa de interés del {tasa_interes}% puede generar un rendimiento anual de ${rendimiento_anual:,.2f} y un beneficio esperado de ${beneficio_esperado:,.2f}."
        print(reporte)
    
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()