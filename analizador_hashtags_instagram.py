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

def main():
    try:
        if len(sys.argv) > 1:
            hashtags = sys.argv[1].split(',')
        else:
            hashtags = ["#mexico", "#instagram", "#marketing", "#python", "#analizador"]
        
        cantidad_hashtags = len(hashtags)
        print(f"Cantidad de hashtags: {cantidad_hashtags}")
        print(f"Hashtags más populares en México: {', '.join(hashtags)}")
        print(f"Fecha de análisis: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        marketing_hashtags = [hashtag for hashtag in hashtags if 'marketing' in hashtag.lower()]
        porcentaje_marketing = (len(marketing_hashtags) / cantidad_hashtags) * 100 if cantidad_hashtags > 0 else 0
        print(f"Porcentaje de hashtags relacionados con marketing: {porcentaje_marketing:.2f}%")
        
        mexico_hashtags = [hashtag for hashtag in hashtags if 'mexico' in hashtag.lower()]
        print(f"Número de hashtags que contienen la palabra 'mexico': {len(mexico_hashtags)}")
        
        top_3_hashtags = sorted(hashtags, key=lambda x: len(x), reverse=True)[:3]
        print(f"Top 3 hashtags más largos: {', '.join(top_3_hashtags)}")
        
        print(f"Hashtags que contienen números: {[hashtag for hashtag in hashtags if any(char.isdigit() for char in hashtag)]}")
        
        print(f"Hashtags que contienen caracteres especiales: {[hashtag for hashtag in hashtags if any(not char.isalnum() and not char.isspace() for char in hashtag)]}")
        
        resumen_ejecutivo = f"Se analizaron {cantidad_hashtags} hashtags, de los cuales {len(marketing_hashtags)} están relacionados con marketing y {len(mexico_hashtags)} contienen la palabra 'mexico'."
        print(f"Resumen ejecutivo: {resumen_ejecutivo}")
    except Exception as e:
        print(f"Error: {str(e)}")
    except ZeroDivisionError:
        print("Error: No se pueden realizar operaciones con division por cero")
    except TypeError:
        print("Error: Tipo de dato incorrecto")

if __name__ == "__main__":
    main()