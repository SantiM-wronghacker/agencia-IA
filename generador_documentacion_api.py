"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza generador documentación api
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Configuración por defecto
        if len(sys.argv) > 1:
            nombre_agencia = sys.argv[1]
        else:
            nombre_agencia = "Agencia Santi"

        if len(sys.argv) > 2:
            ubicacion = sys.argv[2]
        else:
            ubicacion = "México"

        fecha_actual = datetime.datetime.now()
        numeros_aleatorios = [random.randint(1, 100) for _ in range(5)]

        # Generar documentación API
        documentacion = {
            "agencia": nombre_agencia,
            "ubicacion": ubicacion,
            "fecha": fecha_actual.strftime("%Y-%m-%d %H:%M:%S"),
            "numeros": numeros_aleatorios,
            "informacion": [
                {"id": 1, "nombre": "Servicio 1", "descripcion": "Descripción del servicio 1"},
                {"id": 2, "nombre": "Servicio 2", "descripcion": "Descripción del servicio 2"},
                {"id": 3, "nombre": "Servicio 3", "descripcion": "Descripción del servicio 3"}
            ],
            "estadisticas": {
                "promedio_numeros": sum(numeros_aleatorios) / len(numeros_aleatorios),
                "maximo_numero": max(numeros_aleatorios),
                "minimo_numero": min(numeros_aleatorios)
            }
        }

        # Imprimir documentación API
        print("Nombre de la agencia:", documentacion["agencia"])
        print("Ubicación:", documentacion["ubicacion"])
        print("Fecha actual:", documentacion["fecha"])
        print("Números aleatorios:", documentacion["numeros"])
        print("Información de servicios:")
        for servicio in documentacion["informacion"]:
            print(f"ID: {servicio['id']}, Nombre: {servicio['nombre']}, Descripción: {servicio['descripcion']}")
        print("Estadísticas:")
        print(f"Promedio de números: {documentacion['estadisticas']['promedio_numeros']}")
        print(f"Máximo número: {documentacion['estadisticas']['maximo_numero']}")
        print(f"Mínimo número: {documentacion['estadisticas']['minimo_numero']}")
        print("Resumen ejecutivo:")
        print(f"La agencia {documentacion['agencia']} ubicada en {documentacion['ubicacion']} ha generado un informe con {len(documentacion['informacion'])} servicios y {len(documentacion['numeros'])} números aleatorios.")
        print(f"El promedio de los números aleatorios es {documentacion['estadisticas']['promedio_numeros']} y el máximo y mínimo son {documentacion['estadisticas']['maximo_numero']} y {documentacion['estadisticas']['minimo_numero']} respectivamente.")

    except IndexError as e:
        print(f"Error: Debe proporcionar el nombre de la agencia y la ubicación como argumentos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()