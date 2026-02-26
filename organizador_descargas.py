"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Organiza automáticamente la carpeta de Descargas moviendo los archivos por extensión
TECNOLOGÍA: Python, os, shutil
"""

import os
import shutil
import sys
import datetime

def main():
    ruta_descargas = os.path.join(os.path.expanduser('~'), 'Descargas')
    carpetas = {
        'PDF': os.path.join(ruta_descargas, 'PDF'),
        'JPG': os.path.join(ruta_descargas, 'JPG'),
        'PY': os.path.join(ruta_descargas, 'PY')
    }

    for carpeta in carpetas.values():
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def mover_archivos(ruta):
        archivos_movidos = 0
        archivos_no_movidos = 0
        try:
            for archivo in os.listdir(ruta):
                ruta_archivo = os.path.join(ruta, archivo)
                if os.path.isfile(ruta_archivo):
                    extension = os.path.splitext(archivo)[1][1:].upper()
                    if extension == 'PDF':
                        shutil.move(ruta_archivo, carpetas['PDF'])
                        archivos_movidos += 1
                    elif extension == 'JPG' or extension == 'JPEG':
                        shutil.move(ruta_archivo, carpetas['JPG'])
                        archivos_movidos += 1
                    elif extension == 'PY':
                        shutil.move(ruta_archivo, carpetas['PY'])
                        archivos_movidos += 1
                    else:
                        archivos_no_movidos += 1
        except Exception as e:
            print(f"Error al mover archivos: {str(e)}")
        return archivos_movidos, archivos_no_movidos

    archivos_movidos, archivos_no_movidos = mover_archivos(ruta_descargas)
    print(f"Fecha y hora de ejecución: {datetime.datetime.now()}")
    print(f"Ruta de descargas: {ruta_descargas}")
    print(f"Se movieron {archivos_movidos} archivos")
    print(f"Se no se movieron {archivos_no_movidos} archivos")
    print("Archivos organizados correctamente.")
    print("Resumen ejecutivo:")
    print(f"  - Total de archivos movidos: {archivos_movidos}")
    print(f"  - Total de archivos no movidos: {archivos_no_movidos}")
    print(f"  - Ruta de descargas: {ruta_descargas}")

if __name__ == "__main__":
    main()