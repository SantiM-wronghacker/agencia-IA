"""
ÁREA: CEREBRO
DESCRIPCIÓN: Genera un reporte de texto con todas las tareas que el sistema completó durante el día.
TECNOLOGÍA: Python, datetime, sys
"""
from datetime import datetime
import os
import sys
import time

class Tarea:
    def __init__(self, descripcion, tiempo_inicio, tiempo_fin):
        self.descripcion = descripcion
        self.tiempo_inicio = tiempo_inicio
        self.tiempo_fin = tiempo_fin

class ResumenDiarioAgente:
    def __init__(self):
        self.tareas = []

    def agregar_tarea(self, tarea):
        self.tareas.append(tarea)

    def generar_reporte(self):
        reporte = "Resumen diario de tareas\n"
        reporte += "-------------------------\n"
        for tarea in self.tareas:
            reporte += f"Tarea: {tarea.descripcion}\n"
            reporte += f"Tiempo de inicio: {tarea.tiempo_inicio.strftime('%Y-%m-%d %H:%M:%S')}\n"
            reporte += f"Tiempo de fin: {tarea.tiempo_fin.strftime('%Y-%m-%d %H:%M:%S')}\n"
            reporte += "-------------------------\n"

        return reporte

    def guardar_reporte(self, reporte):
        fecha_actual = datetime.now().strftime('%Y-%m-%d')
        nombre_archivo = f"resumen_diario_{fecha_actual}.txt"
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(reporte)

def main():
    agente = ResumenDiarioAgente()

    if len(sys.argv) > 1:
        monto = float(sys.argv[1])
        tasa = float(sys.argv[2])
        plazo = int(sys.argv[3])
    else:
        monto = 2000000
        tasa = 9.5
        plazo = 20
        print(f"Usando valores por defecto: monto={monto}, tasa={tasa}, plazo={plazo}")

    tarea1 = Tarea("Cálculo de hipoteca", datetime(2024, 9, 16, 8, 0, 0), datetime(2024, 9, 16, 9, 0, 0))
    tarea2 = Tarea("Generación de reporte", datetime(2024, 9, 16, 10, 0, 0), datetime(2024, 9, 16, 11, 0, 0))

    agente.agregar_tarea(tarea1)
    agente.agregar_tarea(tarea2)

    reporte = agente.generar_reporte()
    print(reporte)

    time.sleep(2)
    agente.guardar_reporte(reporte)

if __name__ == "__main__":
    main()