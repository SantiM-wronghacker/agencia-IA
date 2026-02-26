"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza analizador cobertura gastos medicos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Parámetros por defecto
        args = sys.argv[1:]
        if len(args) > 0:
            monto_asegurado = float(args[0]) if args[0].replace('.', '').isdigit() else 500000.0
            deducible = float(args[1]) if len(args) > 1 and args[1].replace('.', '').isdigit() else 5000.0
            coaseguro = float(args[2]) if len(args) > 2 and args[2].replace('.', '').isdigit() else 0.10
        else:
            monto_asegurado = 500000.0
            deducible = 5000.0
            coaseguro = 0.10

        # Simulación de gastos médicos
        gastos = {
            "hospitalizacion": random.uniform(10000, 50000),
            "medicamentos": random.uniform(2000, 15000),
            "consultas": random.uniform(500, 3000),
            "laboratorio": random.uniform(1000, 8000),
            "cirugia": random.uniform(0, 100000)
        }

        # Cálculo de cobertura
        total_gastos = sum(gastos.values())
        if total_gastos > monto_asegurado:
            total_gastos = monto_asegurado

        cobertura = total_gastos - deducible
        if cobertura < 0:
            cobertura = 0

        coaseguro_aplicado = cobertura * coaseguro
        cobertura_final = cobertura - coaseguro_aplicado

        # Impresión de resultados
        print(f"Análisis de cobertura de gastos médicos - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Monto asegurado: ${monto_asegurado:,.2f} MXN")
        print(f"Total de gastos médicos: ${total_gastos:,.2f} MXN")
        print(f"Cobertura después de deducible (${deducible:,.2f} MXN): ${cobertura:,.2f} MXN")
        print(f"Coaseguro aplicado ({coaseguro*100:.0f}%): ${coaseguro_aplicado:,.2f} MXN")
        print(f"Cobertura final a pagar: ${cobertura_final:,.2f} MXN")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()