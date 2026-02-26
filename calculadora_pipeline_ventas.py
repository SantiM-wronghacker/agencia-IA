"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza calculadora pipeline ventas
TECNOLOGÍA: Python estándar
"""
import sys
import json
import math
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        ventas_mes_actual = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0
        tasa_conversion = float(sys.argv[2]) if len(sys.argv) > 2 else 0.35
        dias_restantes = int(sys.argv[3]) if len(sys.argv) > 3 else 15
        meta_crecimiento = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0

        # Cálculos
        pipeline_actual = ventas_mes_actual / tasa_conversion
        pipeline_diario = pipeline_actual / dias_restantes
        meta_mes_siguiente = ventas_mes_actual * (1 + (meta_crecimiento / 100))
        pipeline_requerido = meta_mes_siguiente / tasa_conversion
        diferencia_pipeline = pipeline_requerido - pipeline_actual
        tasa_crecimiento = ((meta_mes_siguiente - ventas_mes_actual) / ventas_mes_actual) * 100

        # Salida
        print(f"Fecha: {datetime.now().strftime('%Y-%m-%d')}")
        print(f"Ventas mes actual: ${ventas_mes_actual:,.2f} MXN")
        print(f"Tasa de conversión: {tasa_conversion*100:.2f}%")
        print(f"Días restantes en el mes: {dias_restantes} días")
        print(f"Pipeline actual: ${pipeline_actual:,.2f} MXN")
        print(f"Pipeline diario requerido: ${pipeline_diario:,.2f} MXN")
        print(f"Meta mes siguiente: ${meta_mes_siguiente:,.2f} MXN")
        print(f"Tasa de crecimiento: {meta_crecimiento:.2f}%")
        print(f"Tasa de crecimiento real: {tasa_crecimiento:.2f}%")
        print(f"Diferencia de pipeline a cubrir: ${diferencia_pipeline:,.2f} MXN")
        print(f"Pipeline requerido: ${pipeline_requerido:,.2f} MXN")
        print("Resumen ejecutivo:")
        print(f"Para alcanzar la meta de ${meta_mes_siguiente:,.2f} MXN, se requiere un pipeline de ${pipeline_requerido:,.2f} MXN, lo que representa un aumento de {diferencia_pipeline:,.2f} MXN con respecto al pipeline actual.")

    except IndexError:
        print("Error: No se proporcionaron suficientes parámetros.")
        print("Uso: calculadora_pipeline_ventas.py <ventas_mes_actual> <tasa_conversion> <dias_restantes> <meta_crecimiento>")
        sys.exit(1)
    except ValueError:
        print("Error: Los parámetros proporcionados no son válidos.")
        print("Uso: calculadora_pipeline_ventas.py <ventas_mes_actual> <tasa_conversion> <dias_restantes> <meta_crecimiento>")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()