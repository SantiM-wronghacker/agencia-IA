"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza calculadora regimen fiscal adecuado para México
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_regimen_fiscal(ingreso_anual, deducciones, regimen="general"):
    if regimen == "simplificado":
        tasa_isr = 0.08
    elif regimen == "intermedio":
        tasa_isr = 0.12
    else:  # general
        tasa_isr = 0.15

    base_gravable = max(0, ingreso_anual - deducciones)
    impuesto = base_gravable * tasa_isr
    return impuesto

def calcula_impuesto_marginal(ingreso_anual):
    if ingreso_anual <= 400000:
        return 0.01
    elif ingreso_anual <= 700000:
        return 0.02
    elif ingreso_anual <= 1000000:
        return 0.03
    elif ingreso_anual <= 2000000:
        return 0.04
    elif ingreso_anual <= 5000000:
        return 0.05
    else:
        return 0.06

def calcula_iva(ingreso_anual, tasa_iva=0.16):
    return ingreso_anual * tasa_iva

def main():
    try:
        ingreso_anual = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0
        deducciones = float(sys.argv[2]) if len(sys.argv) > 2 else 100000.0
        regimen = sys.argv[3] if len(sys.argv) > 3 else "general"

        impuesto = calcula_regimen_fiscal(ingreso_anual, deducciones, regimen)
        impuesto_marginal = calcula_impuesto_marginal(ingreso_anual)
        iva = calcula_iva(ingreso_anual)

        print("=== ANÁLISIS FISCAL MEXICANO ===")
        print(f"Ingreso anual: ${ingreso_anual:,.2f}")
        print(f"Deducciones: ${deducciones:,.2f}")
        print(f"Base gravable: ${max(0, ingreso_anual - deducciones):,.2f}")
        print(f"Impuesto sobre la renta (ISR): ${impuesto:,.2f}")
        print(f"Impuesto marginal: {impuesto_marginal*100:.2f}%")
        print(f"IVA estimado: ${iva:,.2f}")
        print(f"Total de impuestos (ISR + IVA): ${impuesto + iva:,.2f}")
        print(f"Porcentaje de impuestos sobre ingreso: {(impuesto + iva) / ingreso_anual * 100:.2f}%")
        print(f"Retención de impuestos (10%): ${ingreso_anual * 0.1:,.2f}")
        print(f"Total de impuestos pagados: ${impuesto + iva + ingreso_anual * 0.1:,.2f}")
        print(f"Total neto después de impuestos: ${ingreso_anual - impuesto - iva:,.2f}")
        print(f"Regimen fiscal aplicado: {regimen.capitalize()}")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Ingreso anual: ${ingreso_anual:,.2f}")
        print(f"Deducciones: ${deducciones:,.2f}")
        print(f"ISR: ${impuesto:,.2f} ({impuesto/ingreso_anual*100:.2f}%)")
        print(f"IVA: ${iva:,.2f} ({iva/ingreso_anual*100:.2f}%)")
        print(f"Total impuestos: ${impuesto + iva:,.2f} ({((impuesto + iva)/ingreso_anual)*100:.2f}%)")
        print(f"Total a pagar después de impuestos: ${ingreso_anual - impuesto - iva:,.2f}")

    except ValueError:
        print("Error: Los valores ingresados deben ser numéricos")