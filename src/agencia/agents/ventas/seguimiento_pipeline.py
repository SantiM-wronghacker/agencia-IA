import os
import sys
import json
from datetime import datetime
import math
import re
import random

try:
    import agencia.agents.herramientas.web_bridge as web
    WEB = web.WEB  # True si hay conexión
except ImportError:
    WEB = False

def seguimiento_pipeline(precios=None, tipo_de_cambio=None, noticias=None):
    if WEB:
        # Busca datos reales con web_bridge (fallback a datos locales si falla)
        try:
            if precios is None:
                resultado = web.buscar("precios de productos Mexico")
                precios = [{"producto": r.get("titulo", "Producto"), "precio": 10000} for r in resultado] if isinstance(resultado, list) else None
            if tipo_de_cambio is None:
                resultado = web.fetch_texto("tipo de cambio USD MXN")
                tipo_de_cambio = float(resultado.get("contenido", "17.0").split()[0]) if isinstance(resultado, dict) and resultado.get("ok") else 17.0
            if noticias is None:
                resultado = web.extraer_precios("noticias economicas Mexico")
                noticias = [{"titulo": f"Noticia {i+1}", "precio": p} for i, p in enumerate(resultado)] if isinstance(resultado, list) else None
        except Exception:
            pass  # Fallback a datos hardcodeados abajo
    # Datos de ejemplo como fallback (independiente de WEB)
    if precios is None:
        precios = [
            {"producto": "Laptop", "precio": 15000},
            {"producto": "Tablet", "precio": 8000},
            {"producto": "Celular", "precio": 12000},
            {"producto": "Consola", "precio": 20000},
            {"producto": "Refrigerador", "precio": 10000},
            {"producto": "Televisor", "precio": 30000},
            {"producto": "Computadora", "precio": 25000},
            {"producto": "Impresora", "precio": 5000},
            {"producto": "Escritorio", "precio": 8000},
            {"producto": "Silla", "precio": 2000}
        ]
    if tipo_de_cambio is None:
        tipo_de_cambio = 1.0
    if noticias is None:
        noticias = [
            {"titulo": "Noticia 1", "precio": 10000},
            {"titulo": "Noticia 2", "precio": 5000},
            {"titulo": "Noticia 3", "precio": 20000},
            {"titulo": "Noticia 4", "precio": 15000},
            {"titulo": "Noticia 5", "precio": 8000},
            {"titulo": "Noticia 6", "precio": 12000},
            {"titulo": "Noticia 7", "precio": 25000},
            {"titulo": "Noticia 8", "precio": 30000},
            {"titulo": "Noticia 9", "precio": 20000},
            {"titulo": "Noticia 10", "precio": 10000}
        ]

    # Calcula ganancias y pérdidas
    ganancias = sum(precio["precio"] for precio in precios)
    pérdidas = sum(noticia["precio"] for noticia in noticias)

    # Convierte ganancias y pérdidas a pesos mexicanos
    ganancias_pesos = ganancias * tipo_de_cambio
    pérdidas_pesos = pérdidas * tipo_de_cambio

    # Imprime resultados
    print(f"ÁREA: VENTAS")
    print(f"DESCRIPCIÓN: Agente que realiza seguimiento pipeline")
    print(f"TECNOLOGÍA: Python estándar, web_bridge (opcional)")
    print(f"Ganancias: ${ganancias_pesos:.2f} MXN")
    print(f"Pérdidas: ${pérdidas_pesos:.2f} MXN")
    print(f"Tipo de cambio: {tipo_de_cambio:.2f}")
    precios_str = ', '.join(f'{p["producto"]}: ${p["precio"]:.2f} MXN' for p in precios)
    noticias_str = ', '.join(f'{n["titulo"]}: ${n["precio"]:.2f} MXN' for n in noticias)
    print(f"Precios de productos: {precios_str}")
    print(f"Noticias: {noticias_str}")
    print(f"Resumen ejecutivo: Las ganancias totales son de ${ganancias_pesos:.2f} MXN, mientras que las pérdidas totales son de ${pérdidas_pesos:.2f} MXN.")

def main():
    try:
        if len(sys.argv) > 1:
            precios = json.loads(sys.argv[1])
            tipo_de_cambio = json.loads(sys.argv[2])
            noticias = json.loads(sys.argv[3])
        else:
            precios = None
            tipo_de_cambio = None
            noticias = None
        seguimiento_pipeline(precios, tipo_de_cambio, noticias)
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()