"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Organiza automáticamente la carpeta de Descargas moviendo los archivos por extensión
TECNOLOGÍA: Python, os, shutil
"""

import os
import shutil
import sys
import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    ruta_descargas = os.path.join(os.path.expanduser('~'), 'Descargas')
    carpetas = {
        'PDF': os.path.join(ruta_descargas, 'PDF'),
        'IMAGENES': os.path.join(ruta_descargas, 'IMAGENES'),
        'CODIGO': os.path.join(ruta_descargas, 'CODIGO')
    }

    if len(sys.argv) > 1:
        ruta_descargas = sys.argv[1]

    for carpeta in carpetas.values():
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def mover_archivos(ruta):
        archivos_movidos = 0
        archivos_no_movidos = 0
        errores = 0
        try:
            for archivo in os.listdir(ruta):
                ruta_archivo = os.path.join(ruta, archivo)
                if os.path.isfile(ruta_archivo):
                    extension = os.path.splitext(archivo)[1][1:].upper()
                    if extension == 'PDF':
                        shutil.move(ruta_archivo, carpetas['PDF'])
                        archivos_movidos += 1
                    elif extension in ['JPG', 'JPEG', 'PNG', 'GIF', 'BMP']:
                        shutil.move(ruta_archivo, carpetas['IMAGENES'])
                        archivos_movidos += 1
                    elif extension in ['PY', 'JAVA', 'CPP', 'C', 'JS']:
                        shutil.move(ruta_archivo, carpetas['CODIGO'])
                        archivos_movidos += 1
                    else:
                        archivos_no_movidos += 1
        except PermissionError:
            errores += 1
            print(f"Error de permiso al mover archivos: {ruta_archivo}")
        except Exception as e:
            errores += 1
            print(f"Error al mover archivos: {str(e)}")
        return archivos_movidos, archivos_no_movidos, errores

    archivos_movidos, archivos_no_movidos, errores = mover_archivos(ruta_descargas)
    print(f"Fecha y hora de ejecución: {datetime.datetime.now()}")
    print(f"Ruta de descargas: {ruta_descargas}")
    print(f"Se movieron {archivos_movidos} archivos")
    print(f"Se no se movieron {archivos_no_movidos} archivos")
    print(f"Se encontraron {errores} errores")
    print("Archivos organizados correctamente.")
    print("Resumen ejecutivo:")
    print(f"  - Total de archivos movidos: {archivos_movidos}")
    print(f"  - Total de archivos no movidos: {archivos_no_movidos}")
    print(f"  - Total de errores: {errores}")

if __name__ == "__main__":
    main()