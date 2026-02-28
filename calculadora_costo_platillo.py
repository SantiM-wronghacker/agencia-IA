"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza calculadora costo platillo
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_costo_platillo(costo_ingrediente, cantidad_ingrediente, precio_venta):
    try:
        costo_total = costo_ingrediente * cantidad_ingrediente
        ganancia = precio_venta - costo_total
        porcentaje_ganancia = (ganancia / costo_total) * 100 if costo_total > 0 else 0
        return costo_total, ganancia, porcentaje_ganancia
    except ZeroDivisionError:
        return None, None, None

def main():
    try:
        # Parámetros por defecto
        costo_ingrediente = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0  # Costo por ingrediente en pesos mexicanos
        cantidad_ingrediente = int(sys.argv[2]) if len(sys.argv) > 2 else 5  # Cantidad de ingredientes
        precio_venta = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0  # Precio de venta del platillo en pesos mexicanos

        if cantidad_ingrediente <= 0:
            print("Error: La cantidad de ingredientes debe ser mayor que cero.")
            return

        if precio_venta <= 0:
            print("Error: El precio de venta del platillo debe ser mayor que cero.")
            return

        costo_total, ganancia, porcentaje_ganancia = calcula_costo_platillo(costo_ingrediente, cantidad_ingrediente, precio_venta)

        if costo_total is None or ganancia is None or porcentaje_ganancia is None:
            print("Error: No se pudo calcular el costo total, la ganancia o el porcentaje de ganancia.")
            return

        print(f"Costo total del platillo: ${costo_total:.2f} MXN")
        print(f"Ganancia por platillo: ${ganancia:.2f} MXN")
        print(f"Porcentaje de ganancia: {porcentaje_ganancia:.2f}%")
        print(f"Precio de venta del platillo: ${precio_venta:.2f} MXN")
        print(f"Margen de ganancia: ${precio_venta - costo_total:.2f} MXN")
        print(f"Costo de ingredientes por platillo: ${costo_ingrediente * cantidad_ingrediente:.2f} MXN")
        print(f"Utilidad neta por platillo: ${ganancia - (costo_total * 0.16):.2f} MXN (considerando 16% de impuestos)")
        print(f"Margen de contribución por platillo: ${ganancia - (costo_total * 0.16):.2f} MXN (considerando 16% de impuestos)")
        print("Resumen ejecutivo:")
        print(f"El platillo tiene un costo total de ${costo_total:.2f} MXN y un precio de venta de ${precio_venta:.2f} MXN, lo que genera una ganancia de ${ganancia:.2f} MXN y un porcentaje de ganancia de {porcentaje_ganancia:.2f}%.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()