"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculadora afore retiro
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        salario = float(sys.argv[2]) if len(sys.argv) > 2 else 15000.0
        aportacion = float(sys.argv[3]) if len(sys.argv) > 3 else 0.065
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.04
        años_retiro = int(sys.argv[5]) if len(sys.argv) > 5 else 25

        if edad < 0 or salario < 0 or aportacion < 0 or tasa_interes < 0 or años_retiro < 0:
            raise ValueError("Los valores no pueden ser negativos")

        ahorro_actual = 0.0
        edad_retiro = edad + años_retiro
        aportacion_mensual = salario * aportacion

        for año in range(edad, edad_retiro):
            ahorro_actual = (ahorro_actual + aportacion_mensual * 12) * (1 + tasa_interes)

        print(f"Edad actual: {edad} años")
        print(f"Edad de retiro: {edad_retiro} años")
        print(f"Ahorro proyectado al retiro: ${math.floor(ahorro_actual)}")
        print(f"Aportación mensual: ${math.floor(aportacion_mensual)}")
        print(f"Tasa de interés anual: {tasa_interes*100}%")
        print(f"Salario mensual: ${math.floor(salario/12)}")
        print(f"Aportación anual: ${math.floor(aportacion_mensual * 12)}")
        print(f"Años hasta el retiro: {años_retiro} años")
        print(f"Total de aportaciones: ${math.floor(aportacion_mensual * 12 * años_retiro)}")
        print("Resumen ejecutivo:")
        print(f"Con una edad actual de {edad} años, un salario de ${math.floor(salario)} al año, una aportación del {aportacion*100}%, una tasa de interés del {tasa_interes*100}% y un retiro en {años_retiro} años, se proyecta un ahorro de ${math.floor(ahorro_actual)} al momento del retiro.")
    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()