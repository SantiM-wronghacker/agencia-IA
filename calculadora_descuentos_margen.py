"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza calculadora descuentos margen
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_descuento(precio, porcentaje):
    return precio * (porcentaje / 100)

def calcula_margen(precio, costo):
    return (precio - costo) / precio * 100

def calcula_iva(precio, porcentaje_iva):
    return precio * (porcentaje_iva / 100)

def main():
    try:
        precio = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
        porcentaje_descuento = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
        costo = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0
        porcentaje_iva = float(sys.argv[4]) if len(sys.argv) > 4 else 16.0

        descuento = calcula_descuento(precio, porcentaje_descuento)
        precio_con_descuento = precio - descuento
        iva = calcula_iva(precio_con_descuento, porcentaje_iva)
        precio_con_iva = precio_con_descuento + iva
        margen = calcula_margen(precio_con_iva, costo + iva)

        print(f"Precio original: ${precio:.2f} MXN")
        print(f"Descuento aplicado: {porcentaje_descuento}%")
        print(f"Descuento calculado: ${descuento:.2f} MXN")
        print(f"Precio con descuento: ${precio_con_descuento:.2f} MXN")
        print(f"IVA aplicado: {porcentaje_iva}%")
        print(f"IVA calculado: ${iva:.2f} MXN")
        print(f"Precio con IVA: ${precio_con_iva:.2f} MXN")
        print(f"Margen calculado: {margen:.2f}%")
        print(f"Costo total (incluyendo IVA): ${costo + iva:.2f} MXN")
        print(f"Utilidad: ${precio_con_iva - (costo + iva):.2f} MXN")
        print(f"Resumen ejecutivo: El precio original de ${precio:.2f} MXN con un descuento de {porcentaje_descuento}% y un IVA de {porcentaje_iva}%, resulta en un precio final de ${precio_con_iva:.2f} MXN, con una utilidad de ${precio_con_iva - (costo + iva):.2f} MXN y un margen de {margen:.2f}%")
        print(f"Porcentaje de utilidad sobre el precio de venta: {(precio_con_iva - (costo + iva)) / precio_con_iva * 100:.2f}%")
        print(f"Porcentaje de utilidad sobre el costo total: {(precio_con_iva - (costo + iva)) / (costo + iva) * 100:.2f}%")
        print(f"Retorno sobre la inversión (ROI): {(precio_con_iva - (costo + iva)) / costo * 100:.2f}%")

    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos")
    except ValueError:
        print("Error: Los argumentos proporcionados no son válidos")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

if __name__ == "__main__":
    main()