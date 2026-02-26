"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora costo empleado mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_costo_empleado(salario_base, horas_trabajadas, dias_trabajados, bonificacion=0):
    salario_diario = salario_base / 30
    costo_por_hora = salario_diario / 8
    subtotal = costo_por_hora * horas_trabajadas * dias_trabajados
    impuesto = subtotal * 0.16  # 16% de impuesto
    seguro_social = subtotal * 0.11  # 11% de seguro social
    infonavit = subtotal * 0.05  # 5% de infonavit
    total = subtotal + impuesto + seguro_social + infonavit + bonificacion
    return subtotal, impuesto, seguro_social, infonavit, total

def main():
    try:
        salario_base = float(sys.argv[1]) if len(sys.argv) > 1 else 25000.0
        horas_trabajadas = float(sys.argv[2]) if len(sys.argv) > 2 else 8.0
        dias_trabajados = float(sys.argv[3]) if len(sys.argv) > 3 else 30.0
        bonificacion = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0

        subtotal, impuesto, seguro_social, infonavit, total = calcular_costo_empleado(salario_base, horas_trabajadas, dias_trabajados, bonificacion)

        print(f"Salario base: ${salario_base:.2f}")
        print(f"Horas trabajadas: {horas_trabajadas:.2f} horas")
        print(f"Días trabajados: {dias_trabajados:.2f} días")
        print(f"Bonificación: ${bonificacion:.2f}")
        print(f"Subtotal: ${subtotal:.2f}")
        print(f"Impuesto (16%): ${impuesto:.2f}")
        print(f"Seguro social (11%): ${seguro_social:.2f}")
        print(f"Infonavit (5%): ${infonavit:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Costo por hora: ${subtotal / (horas_trabajadas * dias_trabajados):.2f}")
        print(f"Costo por día: ${subtotal / dias_trabajados:.2f}")
        print("Resumen ejecutivo:")
        print(f"El costo total del empleado es de ${total:.2f}, con un subtotal de ${subtotal:.2f} y un total de impuestos y contribuciones de ${impuesto + seguro_social + infonavit:.2f}.")

    except ValueError as e:
        print(f"Error: {str(e)}")
    except IndexError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()