"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza comparador instrumentos inversion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        capital = float(sys.argv[1]) if len(sys.argv) > 1 else 10000.0
        plazo = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        tasa_cetes = float(sys.argv[3]) if len(sys.argv) > 3 else 0.11  # 11% anual
        tasa_udibonos = float(sys.argv[4]) if len(sys.argv) > 4 else 0.08  # 8% anual
        tasa_cesd = float(sys.argv[5]) if len(sys.argv) > 5 else 0.09  # 9% anual

        # Cálculos
        rendimiento_cetes = capital * math.pow(1 + tasa_cetes/12, plazo) - capital
        rendimiento_udibonos = capital * math.pow(1 + tasa_udibonos/12, plazo) - capital
        rendimiento_cesd = capital * math.pow(1 + tasa_cesd/12, plazo) - capital
        tasa_inflacion = 0.04  # 4% anual
        rendimiento_real_cetes = rendimiento_cetes - (capital * math.pow(1 + tasa_inflacion/12, plazo) - capital)
        rendimiento_real_udibonos = rendimiento_udibonos - (capital * math.pow(1 + tasa_inflacion/12, plazo) - capital)
        rendimiento_real_cesd = rendimiento_cesd - (capital * math.pow(1 + tasa_inflacion/12, plazo) - capital)

        # Resultados
        print(f"Comparador de instrumentos de inversión (MXN)")
        print(f"Capital inicial: ${capital:,.2f}")
        print(f"Plazo: {plazo} meses")
        print(f"Rendimiento CETES: ${rendimiento_cetes:,.2f} (Tasa: {tasa_cetes*100:.1f}%)")
        print(f"Rendimiento UDIBONOS: ${rendimiento_udibonos:,.2f} (Tasa: {tasa_udibonos*100:.1f}%)")
        print(f"Rendimiento CESD: ${rendimiento_cesd:,.2f} (Tasa: {tasa_cesd*100:.1f}%)")
        print(f"Rendimiento real CETES (ajustado por inflación): ${rendimiento_real_cetes:,.2f}")
        print(f"Rendimiento real UDIBONOS (ajustado por inflación): ${rendimiento_real_udibonos:,.2f}")
        print(f"Rendimiento real CESD (ajustado por inflación): ${rendimiento_real_cesd:,.2f}")
        print(f"Fecha de cálculo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Resumen ejecutivo: El rendimiento más alto es el de {('CETES' if rendimiento_cetes > rendimiento_udibonos and rendimiento_cetes > rendimiento_cesd else 'UDIBONOS' if rendimiento_udibonos > rendimiento_cesd else 'CESD')} con un rendimiento de ${max(rendimiento_cetes, rendimiento_udibonos, rendimiento_cesd):,.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: Falta de parámetros. Uso: python comparador_instrumentos_inversion.py <capital> <plazo> <tasa_cetes> <tasa_udibonos> <tasa_cesd>")

if __name__ == "__main__":
    main()