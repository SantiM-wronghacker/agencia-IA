"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza analizador deuda empresarial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_deuda(total_activos, total_pasivos, deuda_larga_plazo, deuda_corta_plazo):
    return deuda_larga_plazo + deuda_corta_plazo

def calcular_ratio_deuda(total_activos, deuda):
    if total_activos == 0:
        return 0
    return deuda / total_activos

def calcular_costo_deuda(tasa_interes, deuda):
    return deuda * tasa_interes

def calcular_tasa_interes_mensual(tasa_interes_anual):
    return tasa_interes_anual / 12

def calcular_pago_mensual(costo_deuda, plazo_meses):
    return costo_deuda / plazo_meses

def main():
    try:
        total_activos = float(sys.argv[1]) if len(sys.argv) > 1 else 1000000.0
        total_pasivos = float(sys.argv[2]) if len(sys.argv) > 2 else 500000.0
        deuda_larga_plazo = float(sys.argv[3]) if len(sys.argv) > 3 else 200000.0
        deuda_corta_plazo = float(sys.argv[4]) if len(sys.argv) > 4 else 150000.0
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 0.15
        plazo_meses = int(sys.argv[6]) if len(sys.argv) > 6 else 12

        deuda = calcular_deuda(total_activos, total_pasivos, deuda_larga_plazo, deuda_corta_plazo)
        ratio_deuda = calcular_ratio_deuda(total_activos, deuda)
        costo_deuda = calcular_costo_deuda(tasa_interes, deuda)
        tasa_interes_mensual = calcular_tasa_interes_mensual(tasa_interes)
        pago_mensual = calcular_pago_mensual(costo_deuda, plazo_meses)

        print(f"Deuda total: ${deuda:,.2f} MXN")
        print(f"Ratio de deuda: {ratio_deuda:.2%}")
        print(f"Costo de la deuda: ${costo_deuda:,.2f} MXN")
        print(f"Total activos: ${total_activos:,.2f} MXN")
        print(f"Total pasivos: ${total_pasivos:,.2f} MXN")
        print(f"Tasa de interés anual: {tasa_interes*100:.2f}%")
        print(f"Tasa de interés mensual: {tasa_interes_mensual*100:.2f}%")
        print(f"Plazo de pago en meses: {plazo_meses} meses")
        print(f"Pago mensual: ${pago_mensual:,.2f} MXN")
        print(f"Fecha de inicio del pago: {datetime.date.today()}")
        print(f"Fecha de fin del pago: {(datetime.date.today() + datetime.timedelta(days=plazo_meses*30)).strftime('%Y-%m-%d')}")
        print("Resumen ejecutivo:")
        print(f"La empresa tiene una deuda total de ${deuda:,.2f} MXN, con un ratio de deuda del {ratio_deuda:.2%}.")
        print(f"El costo de la deuda es de ${costo_deuda:,.2f} MXN, con un pago mensual de ${pago_mensual:,.2f} MXN durante {plazo_meses} meses.")

    except IndexError:
        print("Error: No se proporcionaron todos los parámetros necesarios.")
    except ValueError:
        print("Error: Los parámetros proporcionados no son válidos.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()