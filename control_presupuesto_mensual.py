"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza control presupuesto mensual
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

def main():
    try:
        # Parámetros por defecto
        presupuesto_mensual = 50000.0  # Pesos mexicanos
        gastos_fijos = 15000.0  # Alquiler, servicios, etc.
        gastos_variables = 10000.0  # Comida, transporte, etc.
        ahorro_mensual = 0.2  # 20% del presupuesto mensual
        tasa_inflacion = 0.03  # 3% anual
        tasa_interes = 0.05  # 5% anual

        # Obtener parámetros desde sys.argv
        if len(sys.argv) > 1:
            presupuesto_mensual = float(sys.argv[1])
        if len(sys.argv) > 2:
            gastos_fijos = float(sys.argv[2])
        if len(sys.argv) > 3:
            gastos_variables = float(sys.argv[3])
        if len(sys.argv) > 4:
            ahorro_mensual = float(sys.argv[4])
        if len(sys.argv) > 5:
            tasa_inflacion = float(sys.argv[5])
        if len(sys.argv) > 6:
            tasa_interes = float(sys.argv[6])

        # Cálculos
        gastos_totales = gastos_fijos + gastos_variables
        ahorro_real = presupuesto_mensual * ahorro_mensual
        disponible = presupuesto_mensual - gastos_totales - ahorro_real
        inflacion_mensual = (1 + tasa_inflacion) ** (1/12) - 1
        interes_mensual = (1 + tasa_interes) ** (1/12) - 1
        valor_ahorro = ahorro_real * (1 + interes_mensual)
        gastos_fijos_con_inflacion = gastos_fijos * (1 + inflacion_mensual)
        gastos_variables_con_inflacion = gastos_variables * (1 + inflacion_mensual)

        # Salida
        print(f"Presupuesto mensual: ${presupuesto_mensual:.2f} MXN")
        print(f"Gastos fijos: ${gastos_fijos:.2f} MXN")
        print(f"Gastos variables: ${gastos_variables:.2f} MXN")
        print(f"Ahorro mensual: ${ahorro_real:.2f} MXN ({ahorro_mensual*100:.0f}%)")
        print(f"Disponible: ${disponible:.2f} MXN")
        print(f"Inflación mensual: {inflacion_mensual*100:.2f}%")
        print(f"Interés mensual: {interes_mensual*100:.2f}%")
        print(f"Valor del ahorro: ${valor_ahorro:.2f} MXN")
        print(f"Gastos fijos con inflación: ${gastos_fijos_con_inflacion:.2f} MXN")
        print(f"Gastos variables con inflación: ${gastos_variables_con_inflacion:.2f} MXN")
        print(f"Resumen ejecutivo: El presupuesto mensual es de ${presupuesto_mensual:.2f} MXN, con gastos fijos de ${gastos_fijos:.2f} MXN y gastos variables de ${gastos_variables:.2f} MXN. El ahorro mensual es de ${ahorro_real:.2f} MXN, con un valor de ${valor_ahorro:.2f} MXN después de aplicar el interés mensual. La inflación mensual es de {inflacion_mensual*100:.2f}% y el interés mensual es de {interes_mensual*100:.2f}%.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()