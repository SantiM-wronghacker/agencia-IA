# CEREBRO - Agente de Fact Checking - Python

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Configuracion por defecto
        pais = 'Mexico'
        poblacion = 127575529
        pib = 1334.78  # Billones de pesos mexicanos

        # Mostrar datos concretos
        print(f"Pais: {pais}")
        print(f"Poblacion: {poblacion}")
        print(f"PIB (billones de pesos mexicanos): {pib}")
        print(f"Fecha actual: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Numero aleatorio entre 1 y 100: {random.randint(1, 100)}")

        # Calculos adicionales
        densidad_poblacional = poblacion / 1964375  # Densidad poblacional por km^2
        print(f"Densidad poblacional (hab/km^2): {densidad_poblacional:.2f}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()