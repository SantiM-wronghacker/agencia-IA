"""
AREA: HERRAMIENTAS
DESCRIPCION: Mueve archivos .bak que tienen más de 24 horas a la carpeta 'Historico'.
TECNOLOGIA: Python, os, shutil, datetime, glob
"""

import os
import shutil
import datetime
import glob
import sys

def mover_archivos_antiguos(ruta_actual, horas_limite=24):
    try:
        ruta_historico = os.path.join(ruta_actual, 'Historico')
        if not os.path.exists(ruta_historico):
            os.makedirs(ruta_historico)
            print(f"Se creó la carpeta {ruta_historico} porque no existía.")

        archivos_bak = glob.glob(os.path.join(ruta_actual, '*.bak'))
        print(f"Se encontraron {len(archivos_bak)} archivos .bak en {ruta_actual}.")

        for archivo in archivos_bak:
            fecha_creacion = datetime.datetime.fromtimestamp(os.path.getctime(archivo))
            diferencia = datetime.datetime.now() - fecha_creacion

            if diferencia > datetime.timedelta(hours=horas_limite):
                nombre_archivo = os.path.basename(archivo)
                ruta_nueva = os.path.join(ruta_historico, nombre_archivo)
                shutil.move(archivo, ruta_nueva)
                print(f"Archivo {nombre_archivo} movido a {ruta_historico} porque tiene {diferencia} de antigüedad.")
            else:
                print(f"Archivo {nombre_archivo} no se movió porque tiene {diferencia} de antigüedad, que es menos de {horas_limite} horas.")

        print(f"Se movieron {sum(1 for archivo in glob.glob(os.path.join(ruta_historico, '*.bak')))} archivos a {ruta_historico}.")
        print(f"Quedan {len(archivos_bak) - sum(1 for archivo in glob.glob(os.path.join(ruta_historico, '*.bak')))} archivos .bak en {ruta_actual}.")

    except Exception as e:
        print(f"Ocurrió un error: {e}")

def main():
    if len(sys.argv) > 1:
        ruta_actual = sys.argv[1]
    else:
        ruta_actual = os.getcwd()
        print("No se proporcionó ruta, utilizando ruta actual por defecto.")
        print(f"Ruta actual: {ruta_actual}")

    if len(sys.argv) > 2:
        horas_limite = int(sys.argv[2])
    else:
        horas_limite = 24
        print("No se proporcionó el límite de horas, utilizando 24 horas por defecto.")

    print(f"Buscando archivos .bak en {ruta_actual}...")
    mover_archivos_antiguos(ruta_actual, horas_limite)

    print("\nResumen ejecutivo:")
    print(f"Ruta actual: {os.getcwd()}")
    print(f"Ruta de búsqueda: {ruta_actual}")
    print(f"Límite de horas: {horas_limite} horas")
    print(f"Archivos .bak encontrados: {len(glob.glob(os.path.join(ruta_actual, '*.bak')))}")
    print(f"Archivos .bak movidos: {sum(1 for archivo in glob.glob(os.path.join(os.path.join(ruta_actual, 'Historico'), '*.bak')))}")

if __name__ == "__main__":
    main()