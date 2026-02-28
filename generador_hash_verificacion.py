"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza generador hash verificacion
TECNOLOGÍA: Python estándar
"""

import sys
import json
import hashlib
import random
import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        num_hash = 5
        longitud_hash = 10
        algoritmo_hash = "sha256"

        # Obtener parámetros de la línea de comandos
        if len(sys.argv) > 1:
            num_hash = int(sys.argv[1])
        if len(sys.argv) > 2:
            longitud_hash = int(sys.argv[2])
        if len(sys.argv) > 3:
            algoritmo_hash = sys.argv[3]

        # Verificar algoritmo de hash válido
        if algoritmo_hash not in ["sha256", "md5", "sha1"]:
            raise ValueError("Algoritmo de hash no válido")

        # Generar hashes de verificación
        hashes = []
        for _ in range(num_hash):
            if algoritmo_hash == "sha256":
                hash_object = hashlib.sha256()
            elif algoritmo_hash == "md5":
                hash_object = hashlib.md5()
            elif algoritmo_hash == "sha1":
                hash_object = hashlib.sha1()
            hash_object.update(str(random.random()).encode('utf-8'))
            hash_hex = hash_object.hexdigest()[:longitud_hash]
            hashes.append(hash_hex)

        # Imprimir resultados
        print("Fecha y hora de generación:", datetime.datetime.now())
        print("Número de hashes generados:", num_hash)
        print("Longitud de cada hash:", longitud_hash)
        print("Algoritmo de hash utilizado:", algoritmo_hash)
        print("Hashes de verificación:")
        for i, hash_value in enumerate(hashes):
            print(f"Hash {i+1}: {hash_value}")
        print("Resumen de operación:")
        print(json.dumps({"num_hash": num_hash, "longitud_hash": longitud_hash, "algoritmo_hash": algoritmo_hash}, indent=4))
        print("Datos adicionales:")
        print("Tiempo de ejecución:", datetime.datetime.now() - datetime.datetime.now())
        print("Número de intentos:", num_hash)
        print("Probabilidad de colisión:", 1 / (16 ** longitud_hash))
        print("Resumen ejecutivo:")
        print("Se han generado {} hashes de verificación utilizando el algoritmo {} con una longitud de {} caracteres.".format(num_hash, algoritmo_hash, longitud_hash))

    except ValueError as e:
        print("Error de valor:", str(e))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()