"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza calculadora costo empleado mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

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
        if len(sys.argv) < 5:
            print("Uso: python calculadora_costo_empleado_mexico.py <salario_base> <horas_trabajadas> <dias_trabajados> <bonificacion>")
            sys.exit(1)

        salario_base = float(sys.argv[1])
        horas_trabajadas = float(sys.argv[2])
        dias_trabajados = float(sys.argv[3])
        bonificacion = float(sys.argv[4])

        if salario_base <= 0 or horas_trabajadas <= 0 or dias_trabajados <= 0:
            print("Error: Los valores de salario base, horas trabajadas y días trabajados deben ser mayores que cero.")
            sys.exit(1)

        subtotal, impuesto, seguro_social, infonavit, total = calcular_costo_empleado(salario_base, horas_trabajadas, dias_trabajados, bonificacion)

        print(f"Resumen de costo del empleado:")
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
        print("\nResumen ejecutivo:")
        print(f"El costo total del empleado es de ${total:.2f}, con un subtotal de ${subtotal:.2f} y un total de impuestos y contribuciones de ${impuesto + seguro_social + infonavit:.2f}.")
        print(f"La bonificación representa el {bonificacion / total * 100:.2f}% del costo total.")
        print(f"El costo por hora es de ${subtotal / (horas_trabajadas * dias_trabajados):.2f}, lo que representa un costo por día de ${subtotal / dias_trabajados:.2f}.")
    except ValueError:
        print("Error: Los valores ingresados deben ser numéricos.")
        sys.exit(1)

if __name__ == "__main__":
    main()