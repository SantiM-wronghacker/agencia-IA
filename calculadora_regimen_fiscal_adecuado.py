"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza calculadora regimen fiscal adecuado
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_regimen_fiscal(ingreso_anual, deducciones):
    tasa_isr = 0.1
    impuesto = (ingreso_anual - deducciones) * tasa_isr
    return impuesto

def calcula_impuesto_marginal(ingreso_anual):
    if ingreso_anual <= 400000:
        return 0.01
    elif ingreso_anual <= 700000:
        return 0.02
    elif ingreso_anual <= 1000000:
        return 0.03
    else:
        return 0.04

def main():
    try:
        ingreso_anual = float(sys.argv[1]) if len(sys.argv) > 1 else 500000.0
        deducciones = float(sys.argv[2]) if len(sys.argv) > 2 else 100000.0
        impuesto = calcula_regimen_fiscal(ingreso_anual, deducciones)
        impuesto_marginal = calcula_impuesto_marginal(ingreso_anual)
        print(f"Ingreso anual: ${ingreso_anual:.2f}")
        print(f"Deducciones: ${deducciones:.2f}")
        print(f"Impuesto sobre la renta (ISR): ${impuesto:.2f}")
        print(f"Impuesto marginal: {impuesto_marginal*100:.2f}%")
        print(f"Total a pagar: ${ingreso_anual - impuesto:.2f}")
        print(f"Porcentaje de impuesto: {impuesto / ingreso_anual * 100:.2f}%")
        print(f"Retención de impuestos: ${ingreso_anual * 0.1:.2f}")
        print(f"Total de impuestos pagados: ${impuesto + ingreso_anual * 0.1:.2f}")
        print(f"Total de impuestos pagados como porcentaje del ingreso: {(impuesto + ingreso_anual * 0.1) / ingreso_anual * 100:.2f}%")
        print("Resumen ejecutivo:")
        print(f"Ingreso anual: ${ingreso_anual:.2f}, Deducciones: ${deducciones:.2f}, Impuesto: ${impuesto:.2f}, Total a pagar: ${ingreso_anual - impuesto:.2f}")
    except ValueError:
        print("Error: Los valores ingresados deben ser numéricos")
    except IndexError:
        print("Error: Debe ingresar el ingreso anual y las deducciones")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()