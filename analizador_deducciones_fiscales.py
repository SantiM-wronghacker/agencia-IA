"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza analizador deducciones fiscales
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime
import random

def main():
    try:
        # Configuración por defecto
        anio_fiscal = datetime.now().year
        deducciones = {
            "gastos_medicos": 50000.00,
            "intereses_hipotecarios": 30000.00,
            "donativos": 15000.00,
            "gastos_educativos": 25000.00,
            "ahorro_voluntario": 10000.00
        }

        # Procesamiento de argumentos
        if len(sys.argv) > 1:
            try:
                anio_fiscal = int(sys.argv[1])
            except ValueError:
                pass

        # Cálculo de deducciones
        total_deducciones = sum(deducciones.values())
        limite_deducciones = 150000.00
        excedente = max(0, total_deducciones - limite_deducciones)

        # Generar reporte
        reporte = {
            "anio_fiscal": anio_fiscal,
            "deducciones_detalladas": deducciones,
            "total_deducciones": round(total_deducciones, 2),
            "limite_deducciones": limite_deducciones,
            "excedente": round(excedente, 2),
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Mostrar resultados
        print(f"Análisis de Deducciones Fiscales {anio_fiscal}")
        print(f"Total de deducciones: ${reporte['total_deducciones']:,.2f}")
        print(f"Límite de deducciones: ${reporte['limite_deducciones']:,.2f}")
        print(f"Excedente no deducible: ${reporte['excedente']:,.2f}")
        print(f"Gastos médicos deducibles: ${deducciones['gastos_medicos']:,.2f}")
        print(f"Intereses hipotecarios deducibles: ${deducciones['intereses_hipotecarios']:,.2f}")

        # Guardar reporte
        with open(f"reporte_deducciones_{anio_fiscal}.json", "w") as f:
            json.dump(reporte, f, indent=4)

    except Exception as e:
        print(f"Error en el análisis: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()