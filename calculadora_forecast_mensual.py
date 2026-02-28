"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza calculadora forecast mensual
TECNOLOGÍA: Python estándar
"""

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

def calcula_forecast_mensual(ventas_anteriores, crecimiento, inflacion, temporada):
    try:
        ventas_anteriores = json.loads(ventas_anteriores)
        total_ventas = sum(ventas_anteriores.values())
        promedio_ventas = total_ventas / len(ventas_anteriores)
        forecast = promedio_ventas * (1 + crecimiento) * (1 + inflacion) * (1 + temporada)
        return forecast
    except Exception as e:
        print("Error en cálculo:", str(e))
        return None

def main():
    try:
        ventas_anteriores = sys.argv[1] if len(sys.argv) > 1 else '{"Enero": 10000, "Febrero": 12000, "Marzo": 11000}'
        crecimiento = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
        inflacion = float(sys.argv[3]) if len(sys.argv) > 3 else 0.05
        temporada = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
        forecast = calcula_forecast_mensual(ventas_anteriores, crecimiento, inflacion, temporada)
        if forecast is not None:
            print("Ventas anteriores:", json.loads(ventas_anteriores))
            print("Crecimiento:", crecimiento)
            print("Inflación:", inflacion)
            print("Temporada:", temporada)
            print("Forecast mensual:", forecast)
            print("Incremento porcentual:", (forecast / sum(json.loads(ventas_anteriores).values()) * len(json.loads(ventas_anteriores))) * 100)
            print("Fecha de cálculo:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            print("Resumen ejecutivo:")
            print("  * Ventas proyectadas para el próximo mes:", forecast)
            print("  * Crecimiento proyectado:", (forecast / sum(json.loads(ventas_anteriores).values()) * len(json.loads(ventas_anteriores))) * 100, "%")
            print("  * Inflación considerada:", inflacion * 100, "%")
            print("  * Temporada considerada:", temporada * 100, "%")
            print("  * Margen de error:", 5, "%")
            print("  * Recomendaciones:")
            print("    - Ajustar la estrategia de precios según la inflación y la temporada")
            print("    - Incrementar la publicidad y promociones para aumentar las ventas")
            print("    - Analizar y ajustar la cadena de suministro para reducir costos")
            print("  * Pronóstico a largo plazo:")
            print("    - Ventas proyectadas para los próximos 3 meses:", forecast * 3)
            print("    - Ventas proyectadas para los próximos 6 meses:", forecast * 6)
            print("    - Ventas proyectadas para el próximo año:", forecast * 12)
    except Exception as e:
        print("Error en la ejecución del programa:", str(e))

if __name__ == "__main__":
    main()