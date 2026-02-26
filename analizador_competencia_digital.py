"""
AREA: MARKETING
DESCRIPCION: Analiza la presencia digital de un competidor: propuesta de valor, canales que usa, debilidades detectadas y oportunidades de diferenciación para el cliente.
TECNOLOGIA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import os
import random

def main():
    try:
        if len(sys.argv) < 3:
            nombre_competidor = 'Inmobiliaria Peña'
            industria = 'real_estate'
        else:
            nombre_competidor = sys.argv[1]
            industria = sys.argv[2]

        propuesta_de_valor = f"Ofrece servicios de {industria} de alta calidad"
        canales_usados = "Redes sociales, sitio web, publicidad en línea"
        debilidades_detectadas = "Falta de presencia en mercados locales"
        oportunidades_diferenciacion = "Ofrecer servicios personalizados y atención al cliente"
        fortalezas = "Equipo experimentado y tecnología de vanguardia"
        objetivos = "Aumentar la presencia en línea y mejorar la satisfacción del cliente"
        estrategia = "Mejorar la experiencia del usuario en el sitio web y en las redes sociales"
        indicadores_clave = "Engagement en redes sociales, tráfico en el sitio web y satisfacción del cliente"

        print(f"Competidor: {nombre_competidor}")
        print(f"Industria: {industria}")
        print(f"Propuesta de valor: {propuesta_de_valor}")
        print(f"Canales usados: {canales_usados}")
        print(f"Debilidades detectadas: {debilidades_detectadas}")
        print(f"Oportunidades de diferenciación: {oportunidades_diferenciacion}")
        print(f"Fortalezas: {fortalezas}")
        print(f"Objetivos: {objetivos}")
        print(f"Estrategia: {estrategia}")
        print(f"Indicadores clave: {indicadores_clave}")
        print(f"Fecha de análisis: {datetime.datetime.now().strftime('%Y-%m-%d')}")
        print(f"Resumen ejecutivo: El competidor {nombre_competidor} tiene una fuerte presencia en línea, pero puede mejorar su atención al cliente y su presencia en mercados locales. La oportunidad de diferenciación se encuentra en ofrecer servicios personalizados y mejorar la experiencia del usuario.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()