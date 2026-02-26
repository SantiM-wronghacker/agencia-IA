"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo depreciacion activos
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calculo_depreciacion(valor_inicial, vida_util, anios_transcurridos):
    depreciacion_acumulada = valor_inicial * (anios_transcurridos / vida_util)
    return depreciacion_acumulada

def main():
    try:
        valor_inicial = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        vida_util = int(sys.argv[2]) if len(sys.argv) > 2 else 5
        anios_transcurridos = int(sys.argv[3]) if len(sys.argv) > 3 else 2

        if vida_util <= 0:
            raise ValueError("La vida útil debe ser mayor que cero")

        if anios_transcurridos < 0:
            raise ValueError("Los años transcurridos no pueden ser negativos")

        if anios_transcurridos > vida_util:
            raise ValueError("Los años transcurridos no pueden superar la vida útil")

        depreciacion_acumulada = calculo_depreciacion(valor_inicial, vida_util, anios_transcurridos)
        valor_actual = valor_inicial - depreciacion_acumulada
        tasa_depreciacion_anual = (depreciacion_acumulada / anios_transcurridos) if anios_transcurridos > 0 else 0
        porcentaje_depreciacion = (depreciacion_acumulada / valor_inicial) * 100 if valor_inicial > 0 else 0

        print(f"Valor Inicial: ${valor_inicial:.2f} MXN")
        print(f"Vida Útil: {vida_util} años")
        print(f"Años Transcurridos: {anios_transcurridos} años")
        print(f"Depreciación Acumulada: ${depreciacion_acumulada:.2f} MXN")
        print(f"Valor Actual: ${valor_actual:.2f} MXN")
        print(f"Tasa Depreciación Anual: ${tasa_depreciacion_anual:.2f} MXN")
        print(f"Porcentaje Depreciación: {porcentaje_depreciacion:.2f}%")
        print(f"Resumen Ejecutivo: El activo ha depreciado un {porcentaje_depreciacion:.2f}% de su valor inicial en {anios_transcurridos} años, con una tasa de depreciación anual de ${tasa_depreciacion_anual:.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()