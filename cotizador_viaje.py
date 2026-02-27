# TURISMO
# Agencia de viajes Way2TheUnknown, cotiza viajes completos con fee del 8%
# Python 3.x

import sys
import json
import datetime
import math
import re
import random
import os

def calcular_precio_base(destino, duracion, tipo_de_viaje):
    precios_base = {
        "nacional": 500,
        "internacional": 1500
    }
    precio = precios_base[tipo_de_viaje] * duracion
    if destino == "Europa":
        precio *= 1.2
    elif destino == "Asia":
        precio *= 1.5
    return precio

def calcular_precio_total(precio_base):
    fee = precio_base * 0.08
    return precio_base + fee

def main():
    try:
        destino = sys.argv[1] if len(sys.argv) > 1 else "Europa"
        duracion = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        tipo_de_viaje = sys.argv[3] if len(sys.argv) > 3 else "internacional"
        
        precio_base = calcular_precio_base(destino, duracion, tipo_de_viaje)
        precio_total = calcular_precio_total(precio_base)
        
        print(f"Destino: {destino}")
        print(f"Duracion: {duracion} dias")
        print(f"Tipo de viaje: {tipo_de_viaje}")
        print(f"Precio base: ${precio_base:.2f}")
        print(f"Precio total con fee del 8%: ${precio_total:.2f}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()