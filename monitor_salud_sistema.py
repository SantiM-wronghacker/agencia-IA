"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza monitor salud sistema
TECNOLOGÍA: Python estándar
"""

import os
import sys
import json
import datetime
import math
import re
import random

def obtener_memoria_total():
    return os.sysconf_names['SC_PAGE_SIZE'] * os.sysconf_names['SC_PHYS_PAGES']

def obtener_memoria_disponible():
    return os.sysconf_names['SC_PAGE_SIZE'] * os.sysconf_names['SC_AVPHYS_PAGES']

def obtener_uptime():
    with open('/proc/uptime', 'r') as f:
        uptime = float(f.readline().split()[0])
        dias = math.floor(uptime / 60 / 60 / 24)
        horas = math.floor((uptime % (60 * 60 * 24)) / 60 / 60)
        minutos = math.floor((uptime % (60 * 60)) / 60)
        return f"{dias} dias, {horas} horas, {minutos} minutos"

def obtener_procesos_actuales():
    return len(os.listdir('/proc')) - 2

def obtener_carga_promedio():
    with open('/proc/loadavg', 'r') as f:
        carga = f.readline().split()
        return carga[0], carga[1], carga[2]

def main():
    try:
        memoria_total = obtener_memoria_total() / (1024 * 1024)
        memoria_disponible = obtener_memoria_disponible() / (1024 * 1024)
        uptime = obtener_uptime()
        procesos_actuales = obtener_procesos_actuales()
        carga_promedio_1min, carga_promedio_5min, carga_promedio_15min = obtener_carga_promedio()

        print(f"Memoria total: {memoria_total:.2f} MB")
        print(f"Memoria disponible: {memoria_disponible:.2f} MB")
        print(f"Uptime: {uptime}")
        print(f"Procesos actuales: {procesos_actuales}")
        print(f"Carga promedio (1min, 5min, 15min): {carga_promedio_1min}, {carga_promedio_5min}, {carga_promedio_15min}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()