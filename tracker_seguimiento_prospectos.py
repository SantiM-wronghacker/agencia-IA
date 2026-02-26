"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza tracker seguimiento prospectos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Parámetros por defecto
        dias_seguimiento = 7
        prospectos_diarios = 10
        tasa_conversion = 0.15  # 15%

        if len(sys.argv) > 1:
            dias_seguimiento = int(sys.argv[1])

        # Generar datos de seguimiento
        fecha_inicio = datetime.now().date()
        prospectos = []
        for dia in range(dias_seguimiento):
            fecha = fecha_inicio + timedelta(days=dia)
            prospectos_dia = random.randint(prospectos_diarios - 2, prospectos_diarios + 2)
            ventas = round(prospectos_dia * tasa_conversion)
            prospectos.append({
                "fecha": fecha.strftime("%Y-%m-%d"),
                "prospectos": prospectos_dia,
                "ventas": ventas,
                "tasa_conversion": round(ventas / prospectos_dia * 100, 2)
            })

        # Calcular métricas
        total_prospectos = sum(p["prospectos"] for p in prospectos)
        total_ventas = sum(p["ventas"] for p in prospectos)
        tasa_conversion_promedio = round(total_ventas / total_prospectos * 100, 2)

        # Mostrar resultados
        print("=== REPORTE DE SEGUIMIENTO DE PROSPECTOS ===")
        print(f"Período: {prospectos[0]['fecha']} al {prospectos[-1]['fecha']}")
        print(f"Prospectos totales: {total_prospectos}")
        print(f"Ventas generadas: {total_ventas}")
        print(f"Tasa de conversión promedio: {tasa_conversion_promedio}%")
        print(f"Prospectos por día: {prospectos_diarios} (promedio)")

    except Exception as e:
        print(f"Error en el seguimiento: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()