"""
ÁREA: CEREBRO
DESCRIPCIÓN: Agente que realiza coordinador pipeline datos
TECNOLOGÍA: Python estándar
"""

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
        # Configuración por defecto
        num_transacciones = int(sys.argv[1]) if len(sys.argv) > 1 else 10
        monto_min = float(sys.argv[2]) if len(sys.argv) > 2 else 100
        monto_max = float(sys.argv[3]) if len(sys.argv) > 3 else 1000

        datos = {
            "fecha": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "monto_total": 0,
            "transacciones": []
        }

        # Simulación de transacciones
        for _ in range(num_transacciones):
            monto = round(random.uniform(monto_min, monto_max), 2)
            datos["monto_total"] += monto
            datos["transacciones"].append({
                "monto": monto,
                "descripcion": f"Transacción {random.randint(1, 100)}"
            })

        # Imprimir resultados
        print(f"Fecha: {datos['fecha']}")
        print(f"Monto total: ${datos['monto_total']:.2f} MXN")
        print(f"Número de transacciones: {len(datos['transacciones'])}")
        print(f"Transacción promedio: ${datos['monto_total'] / len(datos['transacciones']):.2f} MXN")
        print(f"Transacción máxima: ${max(transaccion['monto'] for transaccion in datos['transacciones']):.2f} MXN")
        print(f"Transacción mínima: ${min(transaccion['monto'] for transaccion in datos['transacciones']):.2f} MXN")
        print(f"Desviación estándar: ${math.sqrt(sum((monto - datos['monto_total'] / len(datos['transacciones'])) ** 2 for monto in [transaccion['monto'] for transaccion in datos['transacciones']]) / len(datos['transacciones'])):.2f} MXN")
        print(f"Transacciones:")
        for i, transaccion in enumerate(datos["transacciones"]):
            print(f"  {i+1}. {transaccion['descripcion']}: ${transaccion['monto']:.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"El monto total de las transacciones es de ${datos['monto_total']:.2f} MXN.")
        print(f"El número de transacciones es de {len(datos['transacciones'])}.")
        print(f"La transacción promedio es de ${datos['monto_total'] / len(datos['transacciones']):.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: No se proporcionaron los parámetros necesarios.")
    except ValueError:
        print("Error: Los parámetros proporcionados no son válidos.")

if __name__ == "__main__":
    main()