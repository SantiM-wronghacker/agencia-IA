"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza calculadora licencias software
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math

def main():
    try:
        # Parámetros por línea de comandos con valores por defecto
        args = sys.argv[1:]
        num_licencias = int(args[0]) if len(args) > 0 else 100
        precio_licencia = float(args[1]) if len(args) > 1 else 1500.0
        descuento = float(args[2]) if len(args) > 2 else 0.15

        # Cálculos
        subtotal = num_licencias * precio_licencia
        total_descuento = subtotal * descuento
        total = subtotal - total_descuento
        iva = total * 0.16
        total_final = total + iva

        # Impresión de resultados
        print("Cálculo de licencias de software para Agencia Santi (México)")
        print(f"Número de licencias: {num_licencias}")
        print(f"Precio por licencia: ${precio_licencia:.2f} MXN")
        print(f"Subtotal: ${subtotal:.2f} MXN")
        print(f"Descuento ({descuento*100}%): ${total_descuento:.2f} MXN")
        print(f"Total sin IVA: ${total:.2f} MXN")
        print(f"IVA (16%): ${iva:.2f} MXN")
        print(f"Total con IVA (16%): ${total_final:.2f} MXN")
        print(f"Costo por licencia con IVA: ${total_final/num_licencias:.2f} MXN")
        print(f"Ahorro total por descuento: ${total_descuento:.2f} MXN")
        print(f"Porcentaje de ahorro: {(total_descuento/subtotal)*100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El costo total de las licencias de software es de ${total_final:.2f} MXN.")
        print(f"El descuento aplicado es de ${total_descuento:.2f} MXN, lo que representa un ahorro del {(total_descuento/subtotal)*100:.2f}%.")

    except ValueError as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_licencias_software.py <num_licencias> <precio_licencia> <descuento>")
        print("Ejemplo: calculadora_licencias_software.py 100 1500 0.15")
    except IndexError as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_licencias_software.py <num_licencias> <precio_licencia> <descuento>")
        print("Ejemplo: calculadora_licencias_software.py 100 1500 0.15")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_licencias_software.py <num_licencias> <precio_licencia> <descuento>")
        print("Ejemplo: calculadora_licencias_software.py 100 1500 0.15")

if __name__ == "__main__":
    main()