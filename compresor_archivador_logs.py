"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza compresor archivador logs
TECNOLOGÍA: Python estándar
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
        # Configuración por defecto
        directorio_logs = '/var/log'
        archivo_log = 'log_comprimido.log'
        tamaño_maximo = 1024 * 1024 * 10  # 10 MB

        # Verificar si se han proporcionado argumentos
        if len(sys.argv) > 1:
            directorio_logs = sys.argv[1]
            if len(sys.argv) > 2:
                archivo_log = sys.argv[2]
                if len(sys.argv) > 3:
                    tamaño_maximo = int(sys.argv[3])

        # Comprimir y archivar logs
        archivos_comprimidos = 0
        tamaño_total_comprimido = 0
        for root, dirs, files in os.walk(directorio_logs):
            for file in files:
                if file.endswith('.log'):
                    archivo_log_path = os.path.join(root, file)
                    tamaño_archivo = os.path.getsize(archivo_log_path)
                    if tamaño_archivo > tamaño_maximo:
                        # Comprimir archivo
                        comando_comprimir = f'gzip -c {archivo_log_path} > {archivo_log_path}.gz'
                        os.system(comando_comprimir)
                        tamaño_comprimido = os.path.getsize(f'{archivo_log_path}.gz')
                        tamaño_total_comprimido += tamaño_comprimido
                        archivos_comprimidos += 1
                        print(f'Archivo {file} comprimido con éxito. Tamaño original: {tamaño_archivo} bytes, Tamaño comprimido: {tamaño_comprimido} bytes')
                    else:
                        print(f'Archivo {file} no requiere compresión. Tamaño: {tamaño_archivo} bytes')

        print(f'Total de archivos comprimidos: {archivos_comprimidos}')
        print(f'Tamaño total comprimido: {tamaño_total_comprimido} bytes')
        print(f'Tiempo de ejecución: {datetime.datetime.now()}')
        print(f'Fecha de ejecución: {datetime.date.today()}')
        print(f'Número de archivos en el directorio: {len(os.listdir(directorio_logs))}')

    except Exception as e:
        print(f'Error: {e}')

if __name__ == "__main__":
    main()