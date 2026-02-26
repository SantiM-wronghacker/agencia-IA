"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo impuesto sobre renta mensual
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calculo_impuesto(renta_mensual, deducciones):
    tarifa = 0.1
    if renta_mensual > 50000:
        tarifa = 0.2
    elif renta_mensual > 100000:
        tarifa = 0.3
    impuesto = (renta_mensual - deducciones) * tarifa
    return impuesto

def main():
    try:
        renta_mensual = float(sys.argv[1]) if len(sys.argv) > 1 else 60000
        deducciones = float(sys.argv[2]) if len(sys.argv) > 2 else 10000
        impuesto = calculo_impuesto(renta_mensual, deducciones)
        print(f"Renta mensual: ${renta_mensual:.2f}")
        print(f"Deducciones: ${deducciones:.2f}")
        print(f"Impuesto sobre la renta mensual: ${impuesto:.2f}")
        print(f"Renta neta mensual: ${renta_mensual - impuesto:.2f}")
        print(f"Porcentaje de impuesto sobre la renta mensual: {impuesto / renta_mensual * 100:.2f}%")
        print(f"Impuesto anual estimado: ${impuesto * 12:.2f}")
        print(f"Renta neta anual estimada: ${renta_mensual * 12 - impuesto * 12:.2f}")
        print(f"Porcentaje de impuesto sobre la renta anual: {(impuesto * 12) / (renta_mensual * 12) * 100:.2f}%")
        print(f"Resumen ejecutivo:")
        print(f"  - Renta mensual: ${renta_mensual:.2f}")
        print(f"  - Impuesto mensual: ${impuesto:.2f}")
        print(f"  - Renta neta mensual: ${renta_mensual - impuesto:.2f}")
        print(f"  - Impuesto anual estimado: ${impuesto * 12:.2f}")
        print(f"  - Renta neta anual estimada: ${renta_mensual * 12 - impuesto * 12:.2f}")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()