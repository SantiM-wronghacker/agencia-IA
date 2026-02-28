"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza calculadora costo operacion
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculadora_costo_operacion(costo_producto, cantidad_venta, margen_ganancia, impuestos, tasa_inflacion=0.05):
    costo_total = costo_producto * cantidad_venta
    ganancia = (costo_total * margen_ganancia) / 100
    impuesto = (costo_total * impuestos) / 100
    ajuste_inflacion = (costo_total * tasa_inflacion) / 100
    precio_venta = costo_total + ganancia + impuesto + ajuste_inflacion
    utilidad_neta = precio_venta - costo_total - impuesto
    return {
        "costo_total": round(costo_total, 2),
        "ganancia": round(ganancia, 2),
        "impuesto": round(impuesto, 2),
        "ajuste_inflacion": round(ajuste_inflacion, 2),
        "precio_venta": round(precio_venta, 2),
        "utilidad_neta": round(utilidad_neta, 2)
    }

def main():
    try:
        costo_producto = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
        cantidad_venta = int(sys.argv[2]) if len(sys.argv) > 2 else 100
        margen_ganancia = float(sys.argv[3]) if len(sys.argv) > 3 else 20.0
        impuestos = float(sys.argv[4]) if len(sys.argv) > 4 else 16.0
        tasa_inflacion = float(sys.argv[5]) if len(sys.argv) > 5 else 0.05

        resultado = calculadora_costo_operacion(costo_producto, cantidad_venta, margen_ganancia, impuestos, tasa_inflacion)
        print(f"Costo total: ${resultado['costo_total']}")
        print(f"Ganancia: ${resultado['ganancia']}")
        print(f"Impuesto: ${resultado['impuesto']}")
        print(f"Ajuste por inflación: ${resultado['ajuste_inflacion']}")
        print(f"Precio de venta: ${resultado['precio_venta']}")
        print(f"Utilidad neta: ${resultado['utilidad_neta']}")
        print(f"Margen de utilidad: {(resultado['utilidad_neta'] / resultado['precio_venta']) * 100:.2f}%")
        print(f"Porcentaje de impuesto: {(resultado['impuesto'] / resultado['precio_venta']) * 100:.2f}%")
        print(f"Resumen ejecutivo: El costo total es de ${resultado['costo_total']} y el precio de venta es de ${resultado['precio_venta']}, con una utilidad neta de ${resultado['utilidad_neta']} y un margen de utilidad del {(resultado['utilidad_neta'] / resultado['precio_venta']) * 100:.2f}%")
    except IndexError:
        print("Error: No se proporcionaron suficientes argumentos")
    except ValueError:
        print("Error: Los argumentos proporcionados no son válidos")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()