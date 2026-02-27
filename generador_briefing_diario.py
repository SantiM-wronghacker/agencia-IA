import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        area = 'CEREBRO'
        descripcion = 'Generador de briefing diario'
        tecnologia = 'Python'
        print(f'{area}/{descripcion}/{tecnologia}')

        fecha_actual = datetime.datetime.now()
        print(f'Fecha actual: {fecha_actual.strftime("%Y-%m-%d %H:%M:%S")}')

        temperatura_mexico = round(random.uniform(15, 30), 2)
        humedad_mexico = round(random.uniform(40, 80), 2)
        print(f'Temperatura en México: {temperatura_mexico}°C')
        print(f'Humedad en México: {humedad_mexico}%')

        poblacion_mexico = 127575529
        print(f'Población de México: {poblacion_mexico} habitantes')

        tipo_cambio = round(random.uniform(18, 22), 2)
        print(f'Tipo de cambio (MXN/USD): {tipo_cambio}')

    except Exception as e:
        print(f'Error: {str(e)}')

if __name__ == '__main__':
    main()