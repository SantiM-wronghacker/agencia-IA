"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador promo flash
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def extraer_precios(html):
    precios = []
    try:
        precio = re.findall(r'<span>(\d+\.\d+)</span>', html)
        if precio:
            precios = [float(precio_) for precio_ in precio]
    except Exception as e:
        print(f"Error al extraer precios: {e}")
    return precios

def generar_promo_flash(precio_min=100, precio_max=1000, nombre=None, descripcion=None):
    if nombre is None:
        nombre = "Promo Flash"
    if descripcion is None:
        descripcion = "Oferta especial"
    promo_flash = {
        "nombre": nombre,
        "descripcion": descripcion,
        "precio": round(random.uniform(precio_min, precio_max), 2),
        "fecha_inicio": datetime.date.today(),
        "fecha_fin": datetime.date.today() + datetime.timedelta(days=7)
    }
    return promo_flash

def calcular_beneficio(precio_min, precio_max, precio_promo):
    beneficio_promedio = ((precio_max - precio_promo) * 100 / precio_max)
    beneficio_promedio = round(beneficio_promedio, 2)
    beneficio_promedio = max(0, beneficio_promedio)  # Beneficio no puede ser negativo
    return beneficio_promedio

def resumen_ejecutivo(promo_flash, precios, beneficio_promedio):
    resumen = f"Promo Flash: {promo_flash['nombre']}\n"
    resumen += f"Descripción: {promo_flash['descripcion']}\n"
    resumen += f"Precio: ${promo_flash['precio']:.2f}\n"
    resumen += f"Fecha inicio: {promo_flash['fecha_inicio']}\n"
    resumen += f"Fecha fin: {promo_flash['fecha_fin']}\n"
    resumen += f"Precios encontrados: {', '.join(map(str, precios))}\n"
    resumen += f"Beneficio promedio: {beneficio_promedio}%\n"
    resumen += f"Duración de la promo: {abs((promo_flash['fecha_fin'] - promo_flash['fecha_inicio']).days)} días\n"
    resumen += f"Porcentaje de descuento: {(1 - promo_flash['precio'] / precio_max) * 100:.2f}%\n"
    resumen += f"Total de descuento: ${round((precio_max - promo_flash['precio']), 2)}\n"
    resumen += f"Total de ventas esperadas: ${round(precio_max * 100, 2)}\n"
    return resumen

def main():
    if len(sys.argv) > 1:
        precio_min = float(sys.argv[1])
        precio_max = float(sys.argv[2])
    else:
        precio_min = 100
        precio_max = 1000

    html = "<span>500.00</span><span>200.00</span>"
    precios = extraer_precios(html)
    promo_flash = generar_promo_flash(precio_min, precio_max)
    beneficio_promedio = calcular_beneficio(precio_min, precio_max, promo_flash['precio'])
    resumen = resumen_ejecutivo(promo_flash, precios, beneficio_promedio)
    print(resumen)

if __name__ == "__main__":
    main()