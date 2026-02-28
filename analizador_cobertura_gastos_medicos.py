import sys
import json
import random
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

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
            "hospitalizacion": random.uniform(20000, 80000),
            "medicamentos": random.uniform(5000, 30000),
            "consultas": random.uniform(2000, 10000),
            "laboratorio": random.uniform(3000, 15000),
            "cirugia": random.uniform(50000, 200000)
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
        print(f"Gastos médicos detallados:")
        for gasto, monto in gastos.items():
            print(f"  - {gasto.capitalize()}: ${monto:,.2f} MXN")
        print(f"Cobertura después de deducible (${deducible:,.2f} MXN): ${cobertura:,.2f} MXN")
        print(f"Coaseguro aplicado ({coaseguro*100:.0f}%): ${coaseguro_aplicado:,.2f} MXN")
        print(f"Cobertura final a pagar: ${cobertura_final:,.2f} MXN")
        print(f"Resumen ejecutivo: La cobertura final a pagar es de ${cobertura_final:,.2f} MXN, lo que representa {cobertura_final/monto_asegurado*100:.2f}% del monto asegurado.")

    except ValueError as e:
        print(f"Error: {e}. Por favor, ingrese valores numéricos válidos.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()