"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza simulador fondo emergencia
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import random

def calcular_fondo_emergencia(ingreso_mensual, gastos_fijos, ahorro_mensual, meses):
    fondo_emergencia = 0
    for _ in range(meses):
        fondo_emergencia += ahorro_mensual
        gastos_fijos_mensuales = gastos_fijos / 12
        fondo_emergencia -= gastos_fijos_mensuales
        if fondo_emergencia < 0:
            fondo_emergencia = 0
    return fondo_emergencia

def calcular_interes(fondo_emergencia, tasa_interes, meses):
    interes = fondo_emergencia * tasa_interes / 100 * meses / 12
    return interes

def main():
    try:
        ingreso_mensual = float(sys.argv[1]) if len(sys.argv) > 1 else 25000.0
        gastos_fijos = float(sys.argv[2]) if len(sys.argv) > 2 else 120000.0
        ahorro_mensual = float(sys.argv[3]) if len(sys.argv) > 3 else 5000.0
        meses = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        tasa_interes = float(sys.argv[5]) if len(sys.argv) > 5 else 4.0
        
        fondo_emergencia = calcular_fondo_emergencia(ingreso_mensual, gastos_fijos, ahorro_mensual, meses)
        interes = calcular_interes(fondo_emergencia, tasa_interes, meses)
        
        print(f"Ingreso mensual: ${ingreso_mensual:.2f} MXN")
        print(f"Gastos fijos anuales: ${gastos_fijos:.2f} MXN")
        print(f"Ahorro mensual: ${ahorro_mensual:.2f} MXN")
        print(f"Meses de simulación: {meses} meses")
        print(f"Fondo de emergencia después de {meses} meses: ${fondo_emergencia:.2f} MXN")
        print(f"Interés ganado después de {meses} meses: ${interes:.2f} MXN")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()