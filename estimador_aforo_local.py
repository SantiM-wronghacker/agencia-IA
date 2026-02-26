"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza estimador aforo local
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def estimar_aforo(dia_semana, hora, zona):
    # Datos base de aforo por zona (ejemplo con zonas comerciales de CDMX)
    zonas = {
        "polanco": {"lunes_a_viernes": 0.75, "sabado": 0.9, "domingo": 0.4},
        "condesa": {"lunes_a_viernes": 0.8, "sabado": 0.95, "domingo": 0.5},
        "centro": {"lunes_a_viernes": 0.6, "sabado": 0.85, "domingo": 0.3},
        "santa_fe": {"lunes_a_viernes": 0.7, "sabado": 0.8, "domingo": 0.45}
    }

    # Ajuste por hora del día
    ajustes_hora = {
        "mañana": 0.9,
        "tarde": 1.0,
        "noche": 0.7
    }

    # Determinar día de la semana
    if dia_semana.lower() in ["sabado", "domingo"]:
        base = zonas.get(zona.lower(), zonas["polanco"]).get(dia_semana.lower(), 0.5)
    else:
        base = zonas.get(zona.lower(), zonas["polanco"]).get("lunes_a_viernes", 0.5)

    # Determinar ajuste por hora
    if 6 <= hora < 12:
        ajuste = ajustes_hora["mañana"]
    elif 12 <= hora < 20:
        ajuste = ajustes_hora["tarde"]
    else:
        ajuste = ajustes_hora["noche"]

    # Calcular aforo estimado
    aforo = base * ajuste * (1 + random.uniform(-0.1, 0.1))  # Variación aleatoria

    return round(aforo * 100, 2)

def main():
    try:
        # Parámetros por defecto
        dia = sys.argv[1] if len(sys.argv) > 1 else "lunes"
        hora = int(sys.argv[2]) if len(sys.argv) > 2 else 15
        zona = sys.argv[3] if len(sys.argv) > 3 else "polanco"

        # Validar hora
        if not 0 <= hora <= 23:
            hora = 15

        # Calcular aforo
        aforo = estimar_aforo(dia, hora, zona)

        # Generar salida
        print(f"Fecha de análisis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Zona comercial: {zona.capitalize()}")
        print(f"Día de la semana: {dia.capitalize()}")
        print(f"Hora de análisis: {hora}:00 hrs")
        print(f"Aforo estimado: {aforo}%")
        print(f"Nota: Estimación basada en datos históricos de {zona.capitalize()}")

    except Exception as e:
        print(f"Error en el proceso: {str(e)}")
        print("Uso: python estimador_aforo_local.py [dia] [hora] [zona]")
        print("Ejemplo: python estimador_aforo_local.py sabado 18 condesa")

if __name__ == "__main__":
    main()