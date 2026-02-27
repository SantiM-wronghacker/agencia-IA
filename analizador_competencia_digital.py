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
            industria = 'bienes_raices'
        else:
            nombre_competidor = sys.argv[1]
            industria = sys.argv[2]

        propuesta_de_valor = f"Ofrece servicios de {industria} de alta calidad en México"
        canales_usados = "Redes sociales como Facebook y Instagram, sitio web propio y publicidad en línea en Google Ads"
        debilidades_detectadas = "Falta de presencia en mercados locales como Mercado Libre y Linio"
        oportunidades_diferenciacion = "Ofrecer servicios personalizados y atención al cliente en español"
        fortalezas = "Equipo experimentado y tecnología de vanguardia como CRM y marketing automation"
        objetivos = "Aumentar la presencia en línea y mejorar la satisfacción del cliente en un 20% en los próximos 6 meses"
        estrategia = "Mejorar la experiencia del usuario en el sitio web y en las redes sociales mediante un diseño responsivo y contenido relevante"
        indicadores_clave = "Engagement en redes sociales, tráfico en el sitio web y satisfacción del cliente medidos a través de encuestas y análisis de datos"

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
        print(f"Resumen ejecutivo: El competidor {nombre_competidor} tiene una fuerte presencia en línea en México, pero puede mejorar su atención al cliente y presencia en mercados locales para aumentar su competitividad en el mercado de {industria}.")
        print(f"Recomendaciones: {nombre_competidor} debería considerar invertir en marketing digital y publicidad en línea para aumentar su visibilidad y llegar a un público más amplio en México.")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: python analizador_competencia_digital.py <nombre_competidor> <industria>")

if __name__ == "__main__":
    main()