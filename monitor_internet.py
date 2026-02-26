"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que monitorea la conexión a internet y busca información en Google
TECNOLOGÍA: Python, requests, BeautifulSoup
"""
import os
import platform
import datetime
import time
import requests
from bs4 import BeautifulSoup
import sys

def ping_google():
    if platform.system().lower() == 'windows':
        ping_cmd = ['ping', '-n', '1', 'google.com']
    else:
        ping_cmd = ['ping', '-c', '1', 'google.com']

    response = os.system(' '.join(ping_cmd))
    if response == 0:
        return True
    else:
        return False

def guardar_caida():
    with open('caidas.txt', 'a', encoding='utf-8') as archivo:
        archivo.write(f'{datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n')

def buscar_informacion(busqueda):
    url = "https://www.google.com/search"
    params = {"q": busqueda}
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    try:
        response = requests.get(url, headers=headers, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        resumen = ""
        for i, resultado in enumerate(soup.find_all('h3')):
            if i < 3:
                resumen += f"{i+1}. {resultado.text}\n"
        return resumen
    except Exception as e:
        return f"Error al buscar información: {str(e)}"

def main():
    if len(sys.argv) > 1:
        busqueda = sys.argv[1]
    else:
        busqueda = "inmobiliarias más grandes de México"

    while True:
        if ping_google():
            resumen = buscar_informacion(busqueda)
            print("Conexión a internet establecida. Resumen de la búsqueda:")
            print(resumen)
        else:
            guardar_caida()
            print("No hay conexión a internet. Se ha guardado la caída.")
        time.sleep(2)
        time.sleep(298)  

if __name__ == '__main__':
    main()