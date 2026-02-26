"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza generador propuesta valor
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Parámetros por defecto
        num_propuestas = 5
        monto_minimo = 1000
        monto_maximo = 10000
        descuento_minimo = 0.05
        descuento_maximo = 0.20

        # Obtener parámetros desde la línea de comandos
        if len(sys.argv) > 1:
            num_propuestas = int(sys.argv[1])
        if len(sys.argv) > 2:
            monto_minimo = int(sys.argv[2])
        if len(sys.argv) > 3:
            monto_maximo = int(sys.argv[3])

        # Generar propuestas
        propuestas = []
        for _ in range(num_propuestas):
            monto = round(random.uniform(monto_minimo, monto_maximo), 2)
            descuento = round(random.uniform(descuento_minimo, descuento_maximo), 2)
            ahorro = round(monto * descuento, 2)
            precio_final = round(monto - ahorro, 2)
            propuestas.append({
                "monto": monto,
                "descuento": descuento,
                "ahorro": ahorro,
                "precio_final": precio_final
            })

        # Imprimir propuestas
        print("Propuestas de valor:")
        for i, propuesta in enumerate(propuestas):
            print(f"Propuesta {i+1}:")
            print(f"Monto: ${propuesta['monto']:.2f} MXN")
            print(f"Descuento: {propuesta['descuento']*100:.2f}%")
            print(f"Ahorro: ${propuesta['ahorro']:.2f} MXN")
            print(f"Precio final: ${propuesta['precio_final']:.2f} MXN")
            print()

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()