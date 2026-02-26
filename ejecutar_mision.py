"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Ejecuta una misión de mejora en el Dashboard
TECNOLOGÍA: Python, patcher_pro
"""
from patcher_pro import aplicar_mejora
import os
import time
import sys
import json
import datetime

def procesar(archivo_mision='mision_del_arquitecto.txt', archivo_dashboard='app_dashboard.py'):
    try:
        if not os.path.exists(archivo_mision):
            print(f"No hay archivo de misión: {archivo_mision}")
            return
        
        with open(archivo_mision, 'r', encoding='utf-8') as f:
            mision = f.read()
        
        print(f"Ejecutando misión: {mision}")
        aplicar_mejora(archivo_dashboard, mision)
        time.sleep(2)
        
        print(f"Fecha de ejecución: {datetime.datetime.now()}")
        print(f"Archivo de misión: {archivo_mision}")
        print(f"Archivo de dashboard: {archivo_dashboard}")
        print(f"Estado de la misión: Exitosa")
        
        resumen = {
            "fecha": str(datetime.datetime.now()),
            "archivo_mision": archivo_mision,
            "archivo_dashboard": archivo_dashboard,
            "estado": "Exitosa"
        }
        
        print("\nResumen Ejecutivo:")
        print(json.dumps(resumen, indent=4))
    
    except Exception as e:
        print(f"Error: {str(e)}")
        print(f"Fecha de error: {datetime.datetime.now()}")
        print(f"Archivo de misión: {archivo_mision}")
        print(f"Archivo de dashboard: {archivo_dashboard}")
        print(f"Estado de la misión: Fallida")
        
        resumen = {
            "fecha": str(datetime.datetime.now()),
            "archivo_mision": archivo_mision,
            "archivo_dashboard": archivo_dashboard,
            "estado": "Fallida",
            "error": str(e)
        }
        
        print("\nResumen Ejecutivo:")
        print(json.dumps(resumen, indent=4))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        procesar(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else 'app_dashboard.py')
    else:
        procesar()