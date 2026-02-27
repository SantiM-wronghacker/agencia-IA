# HERRAMIENTAS/MONITOR DE CAMBIOS EN DIRECTORIO/PYTHON

import os
import sys
import json
import datetime
import math
import re
import random

def obtener_directorio_actual():
    return os.getcwd()

def obtener_contenido_directorio(directorio):
    return os.listdir(directorio)

def obtenerInformacionArchivo(archivo):
    estadisticas = os.stat(archivo)
    return {
        'nombre': archivo,
        'tamaño': estadisticas.st_size,
        'fecha_modificacion': datetime.datetime.fromtimestamp(estadisticas.st_mtime)
    }

def main():
    try:
        directorio = sys.argv[1] if len(sys.argv) > 1 else '/home'
        print("Directorio actual:", obtener_directorio_actual())
        print("Directorio a monitorear:", directorio)
        archivos = obtener_contenido_directorio(directorio)
        print("Cantidad de archivos:", len(archivos))
        print("Lista de archivos:")
        for archivo in archivos:
            informacion = obtenerInformacionArchivo(os.path.join(directorio, archivo))
            print(f"Nombre: {informacion['nombre']}, Tamaño: {informacion['tamaño']} bytes, Fecha de modificación: {informacion['fecha_modificacion']}")
    except Exception as e:
        print("Error:", str(e))

if __name__ == '__main__':
    main()