# FINANZAS/Generador Estado Resultados Proyectado/Python

import sys
import json
import datetime
import math
import random

def main():
    try:
        fecha_actual = datetime.date.today()
        año_proyectado = int(sys.argv[1]) if len(sys.argv) > 1 else fecha_actual.year + 1
        ventas_proyectadas = float(sys.argv[2]) if len(sys.argv) > 2 else 1000000.0
        costos_proyectados = float(sys.argv[3]) if len(sys.argv) > 3 else 500000.0
        gastos_proyectados = float(sys.argv[4]) if len(sys.argv) > 4 else 200000.0
        utilidad_proyectada = ventas_proyectadas - costos_proyectados - gastos_proyectados

        print(f"Estado de Resultados Proyectado para el año {año_proyectado}:")
        print(f"Ventas Proyectadas: ${ventas_proyectadas:,.2f} MXN")
        print(f"Costos Proyectados: ${costos_proyectados:,.2f} MXN")
        print(f"Gastos Proyectados: ${gastos_proyectados:,.2f} MXN")
        print(f"Utilidad Proyectada: ${utilidad_proyectada:,.2f} MXN")

    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

if __name__ == '__main__':
    main()