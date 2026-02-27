"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza calculadora ptu empleados
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_ptu(salario_diario, dias_trabajados, dias_incapacidad=0):
    if dias_trabajados <= 0:
        return 0
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    ptu = salario_diario * dias_efectivos * 0.0925
    return ptu

def calcula_isr(salario_diario, dias_trabajados, dias_incapacidad=0):
    dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
    subtotal = salario_diario * dias_efectivos
    if subtotal <= 4160:
        return 0
    elif subtotal <= 6240:
        return subtotal * 0.10
    elif subtotal <= 8640:
        return subtotal * 0.15
    elif subtotal <= 12000:
        return subtotal * 0.20
    else:
        return subtotal * 0.25

def main():
    try:
        salario_diario = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0
        dias_trabajados = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        dias_incapacidad = int(sys.argv[3]) if len(sys.argv) > 3 else 0

        if salario_diario <= 0 or dias_trabajados < 0 or dias_incapacidad < 0:
            raise ValueError("Valores no válidos")

        ptu = calcula_ptu(salario_diario, dias_trabajados, dias_incapacidad)
        isr = calcula_isr(salario_diario, dias_trabajados, dias_incapacidad)
        subtotal = salario_diario * dias_trabajados
        dias_efectivos = max(0, dias_trabajados - dias_incapacidad)
        salario_efectivo = salario_diario * dias_efectivos
        total_con_ptu = subtotal + ptu
        total_con_isr = subtotal - isr
        total_con_ptu_y_isr = subtotal + ptu - isr

        print(f"Salario diario: ${salario_diario:.2f}")
        print(f"Días trabajados: {dias_trabajados}")
        print(f"Días de incapacidad: {dias_incapacidad}")
        print(f"Días efectivos: {dias_efectivos}")
        print(f"Salario efectivo: ${salario_efectivo:.2f}")
        print(f"PTU: ${ptu:.2f}")
        print(f"ISR: ${isr:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Total con PTU: ${total_con_ptu:.2f}")
        print(f"Total con ISR: ${total_con_isr:.2f}")
        print(f"Total con PTU y ISR: ${total_con_ptu_y_isr:.2f}")
        print(f"Resumen Ejecutivo:")
        print(f"  * Salario diario: ${salario_diario:.2f}")
        print(f"  * Días trabajados: {dias_trabajados}")
        print(f"  * Días de incapacidad: {dias_incapacidad}")
        print(f"  * Total con PTU y ISR: ${total_con_ptu_y_isr:.2f}")
        print(f"  * Salario neto promedio diario: ${(total_con_ptu_y_isr / dias_trabajados):.2f}")
        print(f"  * Salario neto promedio efectivo: ${(total_con_ptu_y_isr / dias_efectivos):.2f}")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()