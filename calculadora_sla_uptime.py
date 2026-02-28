import sys
import math
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_sla_uptime(dias_baja=0, horas_baja=0, minutos_baja=0, sla_objetivo=99.9):
    """
    Calcula el SLA y uptime basado en tiempo de baja.
    """
    # Convertir tiempo de baja a segundos
    tiempo_baja_total = dias_baja * 86400 + horas_baja * 3600 + minutos_baja * 60

    # Tiempo total en un año (365 días)
    tiempo_total_anio = 365 * 86400

    # Calcular uptime
    uptime = (tiempo_total_anio - tiempo_baja_total) / tiempo_total_anio * 100

    # Calcular SLA
    sla = min(uptime, sla_objetivo)

    return {
        "tiempo_baja_total": tiempo_baja_total,
        "uptime": round(uptime, 2),
        "sla": round(sla, 2),
        "tiempo_baja_horas": round(tiempo_baja_total / 3600, 2),
        "tiempo_baja_dias": round(tiempo_baja_total / 86400, 2)
    }

def main():
    try:
        # Parámetros por línea de comandos con defaults
        if len(sys.argv) > 1:
            dias_baja = int(sys.argv[1])
        else:
            dias_baja = 0

        if len(sys.argv) > 2:
            horas_baja = int(sys.argv[2])
        else:
            horas_baja = 0

        if len(sys.argv) > 3:
            minutos_baja = int(sys.argv[3])
        else:
            minutos_baja = 0

        if len(sys.argv) > 4:
            sla_objetivo = float(sys.argv[4])
        else:
            sla_objetivo = 99.9

        # Calcular SLA y uptime
        resultados = calcular_sla_uptime(dias_baja, horas_baja, minutos_baja, sla_objetivo)

        # Imprimir resultados
        print("Cálculo de SLA y Uptime para Agencia Santi (México)")
        print(f"Tiempo de baja total: {resultados['tiempo_baja_horas']} horas ({resultados['tiempo_baja_dias']} días)")
        print(f"Uptime anual: {resultados['uptime']}%")
        print(f"SLA alcanzado: {resultados['sla']}% (objetivo: {sla_objetivo}%)")
        print(f"Tiempo de baja en segundos: {resultados['tiempo_baja_total']}")
        print("Resumen Ejecutivo:")
        if resultados['sla'] >= sla_objetivo:
            print(f"El SLA objetivo de {sla_objetivo}% ha sido alcanzado con un uptime de {resultados['uptime']}%.")
        else:
            print(f"El SLA objetivo de {sla_objetivo}% no ha sido alcanzado. El uptime actual es de {resultados['uptime']}%.")

    except ValueError as e:
        print(f"Error en el cálculo: Los parámetros deben ser números enteros o flotantes. {str(e)}")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()