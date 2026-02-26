"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza calculadora punto equilibrio restaurante
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_punto_equilibrio(ventas_diarias, costo_fijo, costo_variable):
    punto_equilibrio = (costo_fijo / (1 - (costo_variable / 100)))
    return punto_equilibrio

def calcular_dias_equilibrio(punto_equilibrio, ventas_diarias):
    return math.ceil(punto_equilibrio / ventas_diarias)

def calcular_margen_contribucion(ventas_diarias, costo_variable):
    return ventas_diarias * (1 - (costo_variable / 100))

def calcular_costo_total(costo_fijo, costo_variable, ventas_diarias):
    return costo_fijo + (costo_variable / 100) * ventas_diarias

def main():
    try:
        ventas_diarias = float(sys.argv[1]) if len(sys.argv) > 1 else 5000.0  # Ventas diarias promedio en pesos mexicanos
        costo_fijo = float(sys.argv[2]) if len(sys.argv) > 2 else 20000.0  # Costo fijo mensual en pesos mexicanos
        costo_variable = float(sys.argv[3]) if len(sys.argv) > 3 else 50.0  # Costo variable como porcentaje de las ventas

        punto_equilibrio = calcular_punto_equilibrio(ventas_diarias, costo_fijo, costo_variable)
        dias_equilibrio = calcular_dias_equilibrio(punto_equilibrio, ventas_diarias)
        margen_contribucion = calcular_margen_contribucion(ventas_diarias, costo_variable)
        costo_total = calcular_costo_total(costo_fijo, costo_variable, ventas_diarias)

        print(f"Ventas diarias promedio: {ventas_diarias} pesos mexicanos")
        print(f"Costo fijo mensual: {costo_fijo} pesos mexicanos")
        print(f"Costo variable: {costo_variable}% de las ventas")
        print(f"Punto de equilibrio: {punto_equilibrio} pesos mexicanos")
        print(f"Días para alcanzar el punto de equilibrio: {dias_equilibrio} días")
        print(f"Margen de contribución: {margen_contribucion} pesos mexicanos")
        print(f"Costo total: {costo_total} pesos mexicanos")
        print(f"Resumen ejecutivo: El restaurante alcanzará el punto de equilibrio en {dias_equilibrio} días, con un margen de contribución de {margen_contribucion} pesos mexicanos y un costo total de {costo_total} pesos mexicanos.")
    except Exception as e:
        print(f"Error: {e}")
    except ValueError:
        print("Error: Los valores ingresados deben ser numéricos.")
    except IndexError:
        print("Error: Debe ingresar los valores de ventas diarias, costo fijo y costo variable.")

if __name__ == "__main__":
    main()