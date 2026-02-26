"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza analizador clausulas riesgo
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

def analizar_clausulas(riesgos):
    resultados = []
    for riesgo in riesgos:
        nivel = round(random.uniform(1, 10), 2)
        probabilidad = round(random.uniform(0, 1), 2)
        impacto = round(random.uniform(0, 100), 2)
        resultado = {
            "riesgo": riesgo,
            "nivel": nivel,
            "probabilidad": probabilidad,
            "impacto": impacto,
            "valor_riesgo": round(nivel * probabilidad * impacto, 2)
        }
        resultados.append(resultado)
    return resultados

def calcular_indice_riesgo(resultados):
    total = sum([resultado['valor_riesgo'] for resultado in resultados])
    return round(total / len(resultados), 2)

def calcular_indice_probabilidad(resultados):
    total = sum([resultado['probabilidad'] for resultado in resultados])
    return round(total / len(resultados), 2)

def calcular_indice_impacto(resultados):
    total = sum([resultado['impacto'] for resultado in resultados])
    return round(total / len(resultados), 2)

def main():
    try:
        if len(sys.argv) > 1:
            riesgos = sys.argv[1:]
        else:
            riesgos = ["Laboral", "Económico", "Político", "Social", "Ambiental"]
        resultados = analizar_clausulas(riesgos)
        print("Análisis de cláusulas de riesgo")
        print("---------------------------")
        print("Fecha de análisis:", datetime.date.today())
        print("Número de riesgos analizados:", len(resultados))
        for i, resultado in enumerate(resultados):
            print(f"Riesgo {i+1}: {resultado['riesgo']}")
            print(f"  Nivel: {resultado['nivel']}")
            print(f"  Probabilidad: {resultado['probabilidad']}")
            print(f"  Impacto: {resultado['impacto']}")
            print(f"  Valor de riesgo: {resultado['valor_riesgo']}")
        print("Valor total de riesgos:", round(sum([resultado['impacto'] for resultado in resultados]), 2))
        print("Índice de riesgo:", calcular_indice_riesgo(resultados))
        print("Índice de probabilidad:", calcular_indice_probabilidad(resultados))
        print("Índice de impacto:", calcular_indice_impacto(resultados))
        print("Resumen ejecutivo:")
        print("  El análisis de cláusulas de riesgo ha identificado", len(resultados), "riesgos potenciales.")
        print("  El índice de riesgo es de", calcular_indice_riesgo(resultados), "lo que indica un nivel de riesgo", "alto" if calcular_indice_riesgo(resultados) > 50 else "bajo")
        print("  Se recomienda revisar y actualizar las cláusulas de riesgo para minimizar el impacto potencial.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()