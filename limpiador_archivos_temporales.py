"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente que realiza limpiador archivos temporales
TECNOLOGIA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        directorio_temp = sys.argv[1] if len(sys.argv) > 1 else '/tmp'
        archivos_eliminados = 0
        espacio_liberado = 0
        espacio_total = 0

        for archivo in os.listdir(directorio_temp):
            ruta_completa = os.path.join(directorio_temp, archivo)
            if os.path.isfile(ruta_completa):
                tamaño_archivo = os.path.getsize(ruta_completa)
                espacio_total += tamaño_archivo
                try:
                    os.remove(ruta_completa)
                    archivos_eliminados += 1
                    espacio_liberado += tamaño_archivo
                except PermissionError:
                    print(f"Error: No se tiene permiso para eliminar el archivo {archivo}")
                except OSError as e:
                    print(f"Error: {str(e)}")

        print(f"Directorio de archivos temporales: {directorio_temp}")
        print(f"Archivos eliminados: {archivos_eliminados}")
        print(f"Espacio liberado: {espacio_liberado / (1024 * 1024):.2f} MB")
        print(f"Espacio total en el directorio: {espacio_total / (1024 * 1024):.2f} MB")
        print(f"Porcentaje de espacio liberado: {(espacio_liberado / espacio_total) * 100 if espacio_total > 0 else 0:.2f}%")
        print(f"Fecha de ejecución: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Versión de Python: {sys.version}")
        print(f"Sistema operativo: {sys.platform}")
        print(f"Nombre del host: {os.uname().nodename if hasattr(os, 'uname') else 'Unknown'}")
        print(f"Resumen ejecutivo: Se eliminaron {archivos_eliminados} archivos y se liberaron {espacio_liberado / (1024 * 1024):.2f} MB de espacio en el directorio {directorio_temp}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()