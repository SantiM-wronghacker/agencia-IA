"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza analizador temporadas
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        año_actual = datetime.now().year
        temporada_alta = [6, 7, 8, 12]  # Junio, julio, agosto, diciembre
        temporada_baja = [1, 2, 3, 4, 5, 9, 10, 11]

        # Generar datos aleatorios de ocupación hotelera (0-100%)
        ocupacion_alta = [random.randint(70, 95) for _ in temporada_alta]
        ocupacion_baja = [random.randint(30, 60) for _ in temporada_baja]

        # Calcular promedios
        promedio_alta = sum(ocupacion_alta) / len(ocupacion_alta)
        promedio_baja = sum(ocupacion_baja) / len(ocupacion_baja)

        # Calcular desviación estándar
        desviacion_alta = (sum((x - promedio_alta) ** 2 for x in ocupacion_alta) / len(ocupacion_alta)) ** 0.5
        desviacion_baja = (sum((x - promedio_baja) ** 2 for x in ocupacion_baja) / len(ocupacion_baja)) ** 0.5

        # Imprimir resultados
        print(f"Análisis de temporadas turísticas {año_actual}")
        print(f"Ocupación promedio temporada alta (meses {temporada_alta}): {promedio_alta:.1f}%")
        print(f"Ocupación promedio temporada baja (meses {temporada_baja}): {promedio_baja:.1f}%")
        print(f"Diferencia entre temporadas: {promedio_alta - promedio_baja:.1f} puntos porcentuales")
        print(f"Desviación estándar temporada alta: {desviacion_alta:.1f}%")
        print(f"Desviación estándar temporada baja: {desviacion_baja:.1f}%")
        print(f"Meses con mayor ocupación: {año_actual}-{temporada_alta[0]:02d} a {año_actual}-{temporada_alta[-1]:02d}")
        print(f"Meses con menor ocupación: {año_actual}-{temporada_baja[0]:02d} a {año_actual}-{temporada_baja[-1]:02d}")
        print(f"Ocupación promedio anual: {(promedio_alta * len(temporada_alta) + promedio_baja * len(temporada_baja)) / 12:.1f}%")
        print(f"Variación porcentual entre temporada alta y baja: {(promedio_alta - promedio_baja) / promedio_baja * 100:.1f}%")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La temporada alta tiene una ocupación promedio de {promedio_alta:.1f}%")
        print(f"La temporada baja tiene una ocupación promedio de {promedio_baja:.1f}%")
        print(f"La diferencia entre temporadas es de {promedio_alta - promedio_baja:.1f} puntos porcentuales")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()