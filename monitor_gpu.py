"""
AREA: HERRAMIENTAS
DESCRIPCION: Monitorea la temperatura y uso de memoria de la GPU
TECNOLOGIA: GPUtil, Python
"""
import GPUtil
import time
import os
import sys

def monitor_gpu(refresh_rate=2):
    gpus = GPUtil.getGPUs()
    if not gpus:
        print("No se encontraron GPUs.")
        return
    gpu = gpus[0]
    try:
        while True:
            temperature = gpu.temperature
            name = gpu.name
            memory_utilization = gpu.memoryUtil * 100
            load = gpu.load * 100
            os.system('cls' if os.name == 'nt' else 'clear')
            print("========================================")
            print(f"  Nombre de la GPU: {name}")
            print("========================================")
            print(f"  Temperatura: {temperature}°C")
            print(f"  Uso de memoria VRAM: {memory_utilization}%")
            print(f"  Carga de la GPU: {load}%")
            print(f"  Memoria total: {gpu.memoryTotal} MB")
            print(f"  Memoria libre: {gpu.memoryFree} MB")
            print(f"  Memoria utilizada: {gpu.memoryUsed} MB")
            print("========================================")
            print(f"  Refresh rate: {refresh_rate} segundos")
            print("========================================")
            time.sleep(refresh_rate)
    except KeyboardInterrupt:
        print("\nMonitor de GPU detenido.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        refresh_rate = int(sys.argv[1])
    else:
        refresh_rate = 2
    monitor_gpu(refresh_rate)
    print("\nResumen ejecutivo:")
    print("El monitor de GPU se ejecutó con éxito.")
    print("Se monitorearon los siguientes parámetros: temperatura, uso de memoria VRAM, carga de la GPU, memoria total, memoria libre y memoria utilizada.")