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

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        num_propuestas = 5
        monto_minimo = 1000
        monto_maximo = 10000
        descuento_minimo = 0.05
        descuento_maximo = 0.20
        iva = 0.16

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
            subtotal = round(monto - ahorro, 2)
            iva_monto = round(subtotal * iva, 2)
            precio_final = round(subtotal + iva_monto, 2)
            propuestas.append({
                "monto": monto,
                "descuento": descuento,
                "ahorro": ahorro,
                "subtotal": subtotal,
                "iva": iva_monto,
                "precio_final": precio_final
            })

        # Imprimir propuestas
        print("Propuestas de valor:")
        for i, propuesta in enumerate(propuestas):
            print(f"Propuesta {i+1}:")
            print(f"Monto: ${propuesta['monto']:.2f} MXN")
            print(f"Descuento: {propuesta['descuento']*100:.2f}%")
            print(f"Ahorro: ${propuesta['ahorro']:.2f} MXN")
            print(f"Subtotal: ${propuesta['subtotal']:.2f} MXN")
            print(f"IVA (16%): ${propuesta['iva']:.2f} MXN")
            print(f"Precio final: ${propuesta['precio_final']:.2f} MXN")
            print(f"Fecha de generación: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print()

        # Resumen ejecutivo
        print("Resumen ejecutivo:")
        print(f"Total de propuestas: {len(propuestas)}")
        print(f"Monto total: ${sum(propuesta['monto'] for propuesta in propuestas):.2f} MXN")
        print(f"Ahorro total: ${sum(propuesta['ahorro'] for propuesta in propuestas):.2f} MXN")
        print(f"Precio final total: ${sum(propuesta['precio_final'] for propuesta in propuestas):.2f} MXN")

    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()