"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza calculadora iva desglosado
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        subtotal = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
        iva = float(sys.argv[2]) if len(sys.argv) > 2 else 16.0
        descuento = float(sys.argv[3]) if len(sys.argv) > 3 else 10.0
        margen_utilidad = float(sys.argv[4]) if len(sys.argv) > 4 else 20.0
        costo_produccion_porcentaje = float(sys.argv[5]) if len(sys.argv) > 5 else 80.0

        importe_iva = (subtotal * iva) / 100
        total = subtotal + importe_iva
        descuento_subtotal = (subtotal * descuento) / 100
        total_con_descuento = total - descuento_subtotal
        margen_utilidad_subtotal = (subtotal * margen_utilidad) / 100
        total_con_margen_utilidad = total + margen_utilidad_subtotal
        costo_produccion = (subtotal * costo_produccion_porcentaje) / 100
        utilidad_neta = total_con_descuento - costo_produccion

        print(f"Subtotal: ${subtotal:.2f}")
        print(f"IVA ({iva}%): ${importe_iva:.2f}")
        print(f"Total: ${total:.2f}")
        print(f"Descuento del {descuento}% sobre el subtotal: ${descuento_subtotal:.2f}")
        print(f"Total con descuento del {descuento}% sobre el subtotal: ${total_con_descuento:.2f}")
        print(f"Margen de utilidad ({margen_utilidad}% sobre el subtotal): ${margen_utilidad_subtotal:.2f}")
        print(f"Total con margen de utilidad ({margen_utilidad}% sobre el subtotal): ${total_con_margen_utilidad:.2f}")
        print(f"Costo de producción ({costo_produccion_porcentaje}% del subtotal): ${costo_produccion:.2f}")
        print(f"Utilidad neta (Total con descuento - Costo de producción): ${utilidad_neta:.2f}")
        print(f"Porcentaje de utilidad neta sobre el subtotal: {(utilidad_neta / subtotal) * 100:.2f}%")
        print(f"Porcentaje de utilidad neta sobre el total con descuento: {(utilidad_neta / total_con_descuento) * 100:.2f}%")
        print(f"Porcentaje de margen de utilidad sobre el subtotal: {(margen_utilidad_subtotal / subtotal) * 100:.2f}%")
        print(f"Porcentaje de costo de producción sobre el subtotal: {(costo_produccion / subtotal) * 100:.2f}%")

        print("\nResumen Ejecutivo:")
        print(f"Total de ventas: ${total:.2f}")
        print(f"Total de descuentos: ${descuento_subtotal:.2f}")
        print(f"Total de utilidad neta: ${utilidad_neta:.2f}")
        print(f"Total de margen de utilidad: ${margen_utilidad_subtotal:.2f}")
        print(f"Total de costo de producción: ${costo_produccion:.2f}")

    except ValueError as e:
        print(f"Error: Valor inválido - {str(e)}")
    except IndexError as e:
        print(f"Error: Parámetro faltante - {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()