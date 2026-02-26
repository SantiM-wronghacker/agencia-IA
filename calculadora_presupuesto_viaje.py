"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza calculadora presupuesto viaje
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def calcula_presupuesto(duracion_viaje, destino, presupuesto_diario):
    presupuesto_total = duracion_viaje * presupuesto_diario
    return presupuesto_total

def calcula_gastos_transporte(duracion_viaje, destino):
    gastos_transporte = 0
    if destino == "nacional":
        gastos_transporte = duracion_viaje * 500
    elif destino == "internacional":
        gastos_transporte = duracion_viaje * 2000
    return gastos_transporte

def calcula_gastos_alimentacion(duracion_viaje, presupuesto_diario):
    gastos_alimentacion = duracion_viaje * (presupuesto_diario * 0.3)
    return gastos_alimentacion

def calcula_gastos_otros(duracion_viaje, presupuesto_diario):
    gastos_otros = duracion_viaje * (presupuesto_diario * 0.2)
    return gastos_otros

def main():
    try:
        duracion_viaje = int(sys.argv[1]) if len(sys.argv) > 1 else 7
        destino = sys.argv[2] if len(sys.argv) > 2 else "nacional"
        presupuesto_diario = int(sys.argv[3]) if len(sys.argv) > 3 else 2000

        presupuesto_total = calcula_presupuesto(duracion_viaje, destino, presupuesto_diario)
        gastos_transporte = calcula_gastos_transporte(duracion_viaje, destino)
        gastos_alimentacion = calcula_gastos_alimentacion(duracion_viaje, presupuesto_diario)
        gastos_otros = calcula_gastos_otros(duracion_viaje, presupuesto_diario)

        print(f"Duración del viaje: {duracion_viaje} días")
        print(f"Destino: {destino}")
        print(f"Presupuesto diario: ${presupuesto_diario}")
        print(f"Presupuesto total: ${presupuesto_total}")
        print(f"Gastos en transporte: ${gastos_transporte}")
        print(f"Gastos en alimentación: ${gastos_alimentacion}")
        print(f"Gastos en otros: ${gastos_otros}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()