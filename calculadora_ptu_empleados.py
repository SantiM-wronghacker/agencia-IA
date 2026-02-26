"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza calculadora ptu empleados
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_ptu(salario_diario, dias_trabajados):
    ptu = salario_diario * dias_trabajados * 0.0925
    return ptu

def calcula_isr(salario_diario, dias_trabajados):
    subtotal = salario_diario * dias_trabajados
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
        ptu = calcula_ptu(salario_diario, dias_trabajados)
        isr = calcula_isr(salario_diario, dias_trabajados)
        subtotal = salario_diario * dias_trabajados
        total_con_ptu = subtotal + ptu
        total_con_isr = subtotal - isr
        total_con_ptu_y_isr = subtotal + ptu - isr
        print(f"Salario diario: ${salario_diario:.2f}")
        print(f"Días trabajados: {dias_trabajados}")
        print(f"PTU: ${ptu:.2f}")
        print(f"ISR: ${isr:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Total con PTU: ${total_con_ptu:.2f}")
        print(f"Total con ISR: ${total_con_isr:.2f}")
        print(f"Total con PTU y ISR: ${total_con_ptu_y_isr:.2f}")
        print(f"Resumen Ejecutivo:")
        print(f"  * Salario diario: ${salario_diario:.2f}")
        print(f"  * Días trabajados: {dias_trabajados}")
        print(f"  * Total con PTU y ISR: ${total_con_ptu_y_isr:.2f}")
    except Exception as e:
        print(f"Error: {str(e)}")
    except ValueError:
        print("Error: Valor no válido")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos")

if __name__ == "__main__":
    main()