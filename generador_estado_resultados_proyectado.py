# FINANZAS/Generador Estado Resultados Proyectado/Python

import sys
import json
import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        fecha_actual = datetime.date.today()
        año_proyectado = int(sys.argv[1]) if len(sys.argv) > 1 else fecha_actual.year + 1
        ventas_proyectadas = float(sys.argv[2]) if len(sys.argv) > 2 else 1000000.0
        costos_proyectados = float(sys.argv[3]) if len(sys.argv) > 3 else 500000.0
        gastos_proyectados = float(sys.argv[4]) if len(sys.argv) > 4 else 200000.0
        impuestos_proyectados = float(sys.argv[5]) if len(sys.argv) > 5 else 0.1 * ventas_proyectadas
        depreciacion_proyectada = float(sys.argv[6]) if len(sys.argv) > 6 else 0.05 * costos_proyectados
        utilidad_proyectada = ventas_proyectadas - costos_proyectados - gastos_proyectados - impuestos_proyectados - depreciacion_proyectada
        margen_utilidad_proyectada = (utilidad_proyectada / ventas_proyectadas) * 100 if ventas_proyectadas > 0 else 0
        roa_proyectado = (utilidad_proyectada / (costos_proyectados + gastos_proyectados)) * 100 if (costos_proyectados + gastos_proyectados) > 0 else 0

        print(f"Estado de Resultados Proyectado para el año {año_proyectado}:")
        print(f"Ventas Proyectadas: ${ventas_proyectadas:,.2f} MXN")
        print(f"Costos Proyectados: ${costos_proyectados:,.2f} MXN")
        print(f"Gastos Proyectados: ${gastos_proyectados:,.2f} MXN")
        print(f"Impuestos Proyectados: ${impuestos_proyectados:,.2f} MXN")
        print(f"Depreciación Proyectada: ${depreciacion_proyectada:,.2f} MXN")
        print(f"Utilidad Proyectada: ${utilidad_proyectada:,.2f} MXN")
        print(f"Márgen de Utilidad Proyectada: {margen_utilidad_proyectada:.2f}%")
        print(f"ROA Proyectado: {roa_proyectado:.2f}%")
        print("Resumen Ejecutivo:")
        print(f"La utilidad proyectada para el año {año_proyectado} es de ${utilidad_proyectada:,.2f} MXN, con un margen de utilidad del {margen_utilidad_proyectada:.2f}% y un ROA del {roa_proyectado:.2f}%.")

    except IndexError:
        print("Faltan argumentos. Por favor, proporcione los siguientes argumentos: año_proyectado, ventas_proyectadas, costos_proyectados, gastos_proyectados, impuestos_proyectados, depreciacion_proyectada")
    except ValueError:
        print("Error en los argumentos. Por favor, proporcione argumentos numéricos.")
    except Exception as e:
        print(f"Ocurrió un error: {str(e)}")

if __name__ == '__main__':
    main()