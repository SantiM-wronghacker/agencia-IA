# TRANSPORTE/Generador de bitacora de vehiculos/Python

import sys
import json
import datetime
import math
import re
import random
import os

def main():
    try:
        # Definir variables
        vehiculos = ["Chevrolet", "Ford", "Toyota", "Volkswagen", "Nissan"]
        placas = ["MX-1234", "MX-5678", "MX-9012", "MX-3456", "MX-7890"]
        kilometrajes = [random.randint(0, 100000) for _ in range(5)]
        fechas = [datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)) for _ in range(5)]

        # Generar bitacora
        print("Bitacora de vehiculos:")
        for i in range(5):
            print(f"Vehiculo: {vehiculos[i]}, Placa: {placas[i]}, Kilometraje: {kilometrajes[i]} km, Fecha: {fechas[i]}")

        # Guardar bitacora en archivo
        with open("bitacora_vehiculos.json", "w") as archivo:
            json.dump({
                "vehiculos": vehiculos,
                "placas": placas,
                "kilometrajes": kilometrajes,
                "fechas": [fecha.isoformat() for fecha in fechas]
            }, archivo, indent=4)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()