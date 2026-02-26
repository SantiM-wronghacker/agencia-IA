"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que busca inmobiliarias más activas en una zona y muestra sus diferenciadores de servicio
TECNOLOGÍA: Python, requests, BeautifulSoup, re
"""

import requests
from bs4 import BeautifulSoup
import re
import sys
import time
from datetime import datetime

def buscar_inmobiliarias(zona, max_results=5):
    try:
        url = f"https://duckduckgo.com/html?q=inmobiliarias+{zona}+mexico"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        inmobiliarias = []
        for result in soup.find_all("a", class_="result__a"):
            link = result.get("href")
            if link:
                title = result.text.strip()
                description = result.find_next("a", class_="result__snippet")
                if description:
                    diferenciador = re.sub(r"<.*?>", "", str(description)).strip()
                    if diferenciador and len(diferenciador) > 10:
                        inmobiliarias.append((title, diferenciador, link))
                        if len(inmobiliarias) >= max_results:
                            break

        return inmobiliarias
    except Exception as e:
        print(f"Error al buscar inmobiliarias: {str(e)}")
        return []

def obtener_diferenciadores(inmobiliarias):
    diferenciadores = []
    for inmobiliaria in inmobiliarias:
        nombre, diferenciador, link = inmobiliaria
        diferenciadores.append((nombre, diferenciador, link))

    return diferenciadores

def generar_resumen(diferenciadores):
    if not diferenciadores:
        return "No se encontraron inmobiliarias relevantes en la zona."

    resumen = []
    resumen.append(f"Análisis de mercado inmobiliario en {sys.argv[1] if len(sys.argv) > 1 else 'Madrid'} (México)")
    resumen.append(f"Fecha del análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    resumen.append(f"Inmobiliarias analizadas: {len(diferenciadores)}")
    resumen.append("Principales diferenciadores detectados:")
    for inmobiliaria in diferenciadores:
        resumen.append(f"- {inmobiliaria[0]}: {inmobiliaria[1][:100]}...")

    return "\n".join(resumen)

def main():
    zona = sys.argv[1] if len(sys.argv) > 1 else "madrid"
    print(f"Analizando mercado inmobiliario en: {zona}")

    inmobiliarias = buscar_inmobiliarias(zona)
    diferenciadores = obtener_diferenciadores(inmobiliarias)

    print("\nInmobiliarias más activas en la zona y sus principales diferenciadores de servicio:")
    for inmobiliaria in diferenciadores:
        print(f"- {inmobiliaria[0]}: {inmobiliaria[1]}")
        print(f"  Enlace: {inmobiliaria[2]}\n")

    print("\n=== Resumen Ejecutivo ===")
    print(generar_resumen(diferenciadores))

if __name__ == "__main__":
    main()