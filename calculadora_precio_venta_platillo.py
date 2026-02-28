"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza calculadora precio venta platillo
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_precio_venta(costo_produccion, margen_ganancia, iva):
    precio_venta = costo_produccion * (1 + margen_ganancia) * (1 + iva)
    return precio_venta

def calcular_utilidad(precio_venta, costo_produccion):
    utilidad = precio_venta - costo_produccion
    return utilidad

def calcular_margen_utilidad(precio_venta, costo_produccion):
    margen_utilidad = (calcular_utilidad(precio_venta, costo_produccion) / precio_venta) * 100
    return margen_utilidad

def main():
    try:
        args = sys.argv
        if len(args) == 4:
            costo_produccion = float(args[1])
            margen_ganancia = float(args[2])
            iva = float(args[3])
        else:
            costo_produccion = 100.0  # default
            margen_ganancia = 0.3  # default
            iva = 0.16  # default

        precio_venta = calcular_precio_venta(costo_produccion, margen_ganancia, iva)
        utilidad = calcular_utilidad(precio_venta, costo_produccion)
        margen_utilidad = calcular_margen_utilidad(precio_venta, costo_produccion)

        print(f"Costo de producción: ${costo_produccion:.2f} MXN")
        print(f"Margen de ganancia: {margen_ganancia*100:.2f}%")
        print(f"IVA: {iva*100:.2f}%")
        print(f"Precio de venta: ${precio_venta:.2f} MXN")
        print(f"Utilidad: ${(utilidad):.2f} MXN")
        print(f"Margen de utilidad: {margen_utilidad:.2f}%")
        print(f"Porcentaje de costo de producción sobre el precio de venta: {(costo_produccion / precio_venta) * 100:.2f}%")
        print(f"Porcentaje de utilidad sobre el precio de venta: {(utilidad / precio_venta) * 100:.2f}%")
        print(f"Porcentaje de IVA sobre el precio de venta: {(iva * costo_produccion * (1 + margen_ganancia)) / precio_venta * 100:.2f}%")

        print("\nResumen Ejecutivo:")
        print(f"El precio de venta del platillo es de ${precio_venta:.2f} MXN, con una utilidad de ${(utilidad):.2f} MXN y un margen de utilidad de {margen_utilidad:.2f}%.")

    except ValueError as e:
        print(f"Error: {e}")
    except IndexError:
        print("Error: No se proporcionaron los argumentos necesarios. Uso: python calculadora_precio_venta_platillo.py <costo_produccion> <margen_ganancia> <iva>")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()