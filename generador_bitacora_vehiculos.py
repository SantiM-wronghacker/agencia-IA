# TRANSPORTE/Generador de bitacora de vehiculos/Python

import sys
import json
import datetime
import math
import re
import random
import os

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Definir variables
        num_vehiculos = 10
        vehiculos = ["Chevrolet", "Ford", "Toyota", "Volkswagen", "Nissan", "Honda", "Kia", "Hyundai", "Mazda", "BMW"]
        placas = [f"MX-{random.randint(1000, 9999)}" for _ in range(num_vehiculos)]
        kilometrajes = [random.randint(0, 200000) for _ in range(num_vehiculos)]
        fechas = [datetime.date.today() - datetime.timedelta(days=random.randint(0, 365)) for _ in range(num_vehiculos)]
        combustibles = ["Gasolina", "Diesel", "Gas", "Electrico"]
        tipos_vehiculos = ["Automovil", "Camioneta", "Camion", "Motocicleta"]

        # Generar bitacora
        print("Bitacora de vehiculos:")
        for i in range(num_vehiculos):
            print(f"Vehiculo: {vehiculos[i]}, Placa: {placas[i]}, Kilometraje: {kilometrajes[i]} km, Fecha: {fechas[i]}, Combustible: {random.choice(combustibles)}, Tipo: {random.choice(tipos_vehiculos)}")

        # Calcular estadisticas
        total_kilometraje = sum(kilometrajes)
        promedio_kilometraje = total_kilometraje / num_vehiculos
        max_kilometraje = max(kilometrajes)
        min_kilometraje = min(kilometrajes)

        # Imprimir estadisticas
        print("\nEstadisticas:")
        print(f"Total kilometraje: {total_kilometraje} km")
        print(f"Promedio kilometraje: {promedio_kilometraje:.2f} km")
        print(f"Maximo kilometraje: {max_kilometraje} km")
        print(f"Minimo kilometraje: {min_kilometraje} km")

        # Guardar bitacora en archivo
        with open("bitacora_vehiculos.json", "w") as archivo:
            json.dump({
                "vehiculos": vehiculos,
                "placas": placas,
                "kilometrajes": kilometrajes,
                "fechas": [fecha.isoformat() for fecha in fechas],
                "combustibles": [random.choice(combustibles) for _ in range(num_vehiculos)],
                "tipos_vehiculos": [random.choice(tipos_vehiculos) for _ in range(num_vehiculos)]
            }, archivo, indent=4)

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print("Se ha generado una bitacora de vehiculos con 10 registros.")
        print("Los datos incluyen el tipo de vehiculo, placa, kilometraje, fecha, combustible y tipo de vehiculo.")
        print("Se han calculado estadisticas como el total y promedio de kilometraje, asi como el maximo y minimo.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()