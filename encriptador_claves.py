"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Encriptador de claves para archivos de texto
TECNOLOGÍA: Python, cryptography
"""

from cryptography.fernet import Fernet
import base64
import os
import sys
import time
import json
import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_llave_secreta():
    try:
        llave = Fernet.generate_key()
        return llave
    except Exception as e:
        print(f"Error al generar llave secreta: {e}")
        return None

def encriptar_archivo(archivo, llave):
    try:
        f = Fernet(llave)
        with open(archivo, "rb") as file:
            archivo_data = file.read()
        encrypted_data = f.encrypt(archivo_data)
        with open(archivo, "wb") as file:
            file.write(encrypted_data)
        return True
    except Exception as e:
        print(f"Error al encriptar archivo: {e}")
        return False

def desencriptar_archivo(archivo, llave):
    try:
        f = Fernet(llave)
        with open(archivo, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = f.decrypt(encrypted_data)
        with open(archivo, "wb") as file:
            file.write(decrypted_data)
        return True
    except Exception as e:
        print(f"Error al desencriptar archivo: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        archivo_path = "claves.txt"
        contenido_archivo = "API_KEY=mi_api_key_secreta"
    else:
        archivo_path = sys.argv[1]
        contenido_archivo = sys.argv[2] if len(sys.argv) > 2 else "API_KEY=mi_api_key_secreta"

    llave_secreta = generar_llave_secreta()
    if llave_secreta is None:
        return

    print("Llave secreta:", llave_secreta)
    print("Fecha y hora actual:", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("Archivo a encriptar:", archivo_path)
    print("Contenido del archivo:", contenido_archivo)

    with open(archivo_path, "w", encoding='utf-8') as file:
        file.write(contenido_archivo)
    if encriptar_archivo(archivo_path, llave_secreta):
        print("Archivo encriptado con éxito.")
    else:
        print("Error al encriptar archivo.")
        return

    time.sleep(2)

    if desencriptar_archivo(archivo_path, llave_secreta):
        print("Archivo desencriptado con éxito.")
    else:
        print("Error al desencriptar archivo.")
        return

    with open(archivo_path, "r", encoding='utf-8') as file:
        contenido_archivo = file.read()
    print("Contenido del archivo desencriptado:", contenido_archivo)
    print("Tamaño del archivo:", os.path.getsize(archivo_path), "bytes")
    print("Resumen ejecutivo:")
    print(json.dumps({
        "llave_secreta": llave_secreta.decode("utf-8"),
        "archivo_path": archivo_path,
        "contenido_archivo": contenido_archivo,
        "fecha_y_hora": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, indent=4))

if __name__ == "__main__":
    main()