#!/usr/bin/env python
"""Check which api_agencia.py file is being used
AREA: HERRAMIENTAS
DESCRIPCION: Verificar la existencia y contenido del archivo api_agencia.py
TECNOLOGIA: Python"""
import sys
import os
import datetime
import math

# Add current dir to path
sys.path.insert(0, os.getcwd())

def main():
    try:
        # Check file location
        api_path = os.path.join(os.getcwd(), 'api_agencia.py')
        print(f"Current directory: {os.getcwd()}")
        print(f"API file path: {api_path}")
        print(f"File exists: {os.path.exists(api_path)}")

        if os.path.exists(api_path):
            with open(api_path, 'r', encoding='utf-8') as f:
                content = f.read()

            has_test = '/test-19-cats' in content
            print(f"\n/test-19-cats endpoint exists: {has_test}")

            # Find the position
            if has_test:
                idx = content.find('/test-19-cats')
                section = content[max(0, idx-200):idx+500]
                print(f"\nContext around /test-19-cats:")
                print(section)

            # Calculate file size in megabytes
            file_size_bytes = os.path.getsize(api_path)
            file_size_mb = math.ceil(file_size_bytes / (1024 * 1024))
            print(f"\nAPI file size: {file_size_mb} MB")

            # Calculate file modification time
            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(api_path))
            print(f"API file modification time: {mod_time}")

            # Get file permissions
            permissions = oct(os.stat(api_path).st_mode)[-3:]
            print(f"API file permissions: {permissions}")

            # Get file owner
            owner = os.stat(api_path).st_uid
            print(f"API file owner: {owner}")

            # Get file last access time
            last_access_time = datetime.datetime.fromtimestamp(os.path.getatime(api_path))
            print(f"API file last access time: {last_access_time}")

            # Get file last modification time
            last_modification_time = datetime.datetime.fromtimestamp(os.path.getmtime(api_path))
            print(f"API file last modification time: {last_modification_time}")

        else:
            print("\nEl archivo api_agencia.py no existe en el directorio actual.")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
    except PermissionError as e:
        print(f"\nError: {e}")
    except Exception as e:
        print(f"\nError: {e}")

    print("\nResumen ejecutivo:")
    print("Se ha verificado la existencia y contenido del archivo api_agencia.py.")
    print("Se han obtenido los metadatos del archivo, como tamaño, fecha de modificación, permisos, propietario, última accesión, última modificación.")
    print("Se ha buscado la presencia del endpoint /test-19-cats en el archivo.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print("Usage: python check_api_code.py")
        print("Options:")
        print("  --help  Show this message and exit")
    else:
        main()