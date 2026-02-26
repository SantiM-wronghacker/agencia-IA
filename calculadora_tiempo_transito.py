"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora tiempo transito
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime, timedelta

def calcular_tiempo_transito():
    # Parámetros por defecto (ejemplo realista para México)
    distancia_km = 500
    velocidad_promedio = 80  # km/h
    tiempo_espera = 2  # horas

    if len(sys.argv) > 1:
        try:
            distancia_km = float(sys.argv[1])
        except ValueError:
            pass

    if len(sys.argv) > 2:
        try:
            velocidad_promedio = float(sys.argv[2])
        except ValueError:
            pass

    if len(sys.argv) > 3:
        try:
            tiempo_espera = float(sys.argv[3])
        except ValueError:
            pass

    tiempo_conduccion = distancia_km / velocidad_promedio
    tiempo_total = tiempo_conduccion + tiempo_espera
    fecha_hora_actual = datetime.now()
    fecha_hora_llegada = fecha_hora_actual + timedelta(hours=tiempo_total)

    return {
        "distancia_km": distancia_km,
        "velocidad_promedio": velocidad_promedio,
        "tiempo_conduccion_horas": round(tiempo_conduccion, 2),
        "tiempo_espera_horas": tiempo_espera,
        "tiempo_total_horas": round(tiempo_total, 2),
        "fecha_hora_actual": fecha_hora_actual.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_hora_llegada": fecha_hora_llegada.strftime("%Y-%m-%d %H:%M:%S")
    }

def main():
    try:
        resultado = calcular_tiempo_transito()
        print("=== CÁLCULO DE TIEMPO DE TRÁNSITO ===")
        print(f"Distancia: {resultado['distancia_km']} km")
        print(f"Velocidad promedio: {resultado['velocidad_promedio']} km/h")
        print(f"Tiempo de conducción: {resultado['tiempo_conduccion_horas']} horas")
        print(f"Tiempo de espera: {resultado['tiempo_espera_horas']} horas")
        print(f"Tiempo total estimado: {resultado['tiempo_total_horas']} horas")
        print(f"Fecha y hora actual: {resultado['fecha_hora_actual']}")
        print(f"Fecha y hora estimada de llegada: {resultado['fecha_hora_llegada']}")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()