"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador calendario editorial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import random
import os

def generar_calendario_editorial(anio=datetime.datetime.now().year):
    meses = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    eventos = [
        {"nombre": "Día de la Independencia", "fecha": "16 de septiembre"},
        {"nombre": "Día de Muertos", "fecha": "2 de noviembre"},
        {"nombre": "Navidad", "fecha": "25 de diciembre"},
        {"nombre": "Día del Niño", "fecha": "30 de abril"},
        {"nombre": "Día de la Madre", "fecha": "10 de mayo"}
    ]

    calendario = []
    for mes in meses:
        eventos_mes = [e for e in eventos if e["fecha"].split()[1] == mes]
        calendario.append({
            "mes": mes,
            "eventos": eventos_mes,
            "presupuesto": random.randint(5000, 20000),
            "publicaciones": random.randint(3, 8)
        })

    return calendario

def main():
    try:
        if len(sys.argv) > 1:
            anio = int(sys.argv[1])
        else:
            anio = datetime.datetime.now().year

        calendario = generar_calendario_editorial(anio)

        for mes in calendario:
            print(f"Mes: {mes['mes']}")
            print(f"Eventos: {', '.join([e['nombre'] for e in mes['eventos']])}")
            print(f"Presupuesto asignado: ${mes['presupuesto']:.2f} MXN")
            print(f"Publicaciones planificadas: {mes['publicaciones']}")
            print("-" * 40)

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()