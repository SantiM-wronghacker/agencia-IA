"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza analizador hashtags instagram
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def obtener_hashtags():
    if len(sys.argv) > 1:
        return sys.argv[1].split(',')
    else:
        return ["#mexico", "#instagram", "#marketing", "#python", "#analizador", "#mexicomarketing", "#mexicodigital", "#mexicoinstagram", "#mexicoinfluencer"]

def calcular_porcentaje_marketing(hashtags):
    marketing_hashtags = [hashtag for hashtag in hashtags if 'marketing' in hashtag.lower()]
    return (len(marketing_hashtags) / len(hashtags)) * 100 if len(hashtags) > 0 else 0

def calcular_porcentaje_mexico(hashtags):
    mexico_hashtags = [hashtag for hashtag in hashtags if 'mexico' in hashtag.lower()]
    return (len(mexico_hashtags) / len(hashtags)) * 100 if len(hashtags) > 0 else 0

def obtener_top_3_hashtags_largos(hashtags):
    return sorted(hashtags, key=lambda x: len(x), reverse=True)[:3]

def obtener_hashtags_con_numeros(hashtags):
    return [hashtag for hashtag in hashtags if any(char.isdigit() for char in hashtag)]

def obtener_hashtags_con_caracteres_especiales(hashtags):
    return [hashtag for hashtag in hashtags if any(not char.isalnum() and not char.isspace() for char in hashtag)]

def main():
    try:
        hashtags = obtener_hashtags()
        cantidad_hashtags = len(hashtags)
        
        print(f"Cantidad de hashtags: {cantidad_hashtags}")
        print(f"Hashtags más populares en México: {', '.join(hashtags)}")
        print(f"Fecha de análisis: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        porcentaje_marketing = calcular_porcentaje_marketing(hashtags)
        print(f"Porcentaje de hashtags relacionados con marketing: {porcentaje_marketing:.2f}%")
        
        porcentaje_mexico = calcular_porcentaje_mexico(hashtags)
        print(f"Porcentaje de hashtags que contienen la palabra 'mexico': {porcentaje_mexico:.2f}%")
        
        top_3_hashtags_largos = obtener_top_3_hashtags_largos(hashtags)
        print(f"Top 3 hashtags más largos: {', '.join(top_3_hashtags_largos)}")
        
        hashtags_con_numeros = obtener_hashtags_con_numeros(hashtags)
        print(f"Hashtags que contienen números: {', '.join(hashtags_con_numeros)}")
        
        hashtags_con_caracteres_especiales = obtener_hashtags_con_caracteres_especiales(hashtags)
        print(f"Hashtags que contienen caracteres especiales: {', '.join(hashtags_con_caracteres_especiales)}")
        
        resumen_ejecutivo = f"Se analizaron {cantidad_hashtags} hashtags, de los cuales {int(porcentaje_marketing)}% están relacionados con marketing y {int(porcentaje_mexico)}% contienen la palabra 'mexico'."
        print(f"Resumen ejecutivo: {resumen_ejecutivo}")
    except Exception as e:
        print(f"Error: {str(e)}")
        print("Se produjo un error al ejecutar el análisis de hashtags.")

if __name__ == "__main__":
    main()