"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza convenio prestacion servicios
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import random
import os
import math

def generar_convenio(monto_min=50000, monto_max=500000, duracion_min=3, duracion_max=24):
    datos = {
        "fecha": datetime.datetime.now().strftime("%d/%m/%Y"),
        "numero_convenio": f"CONV-{random.randint(1000, 9999)}",
        "monto": round(random.uniform(monto_min, monto_max), 2),
        "duracion_meses": random.randint(duracion_min, duracion_max),
        "partes": ["Agencia Santi", "Cliente " + str(random.randint(1, 1000))],
        "impuesto": round(datos["monto"] * 0.16, 2),  # IVA 16%
        "total": round(datos["monto"] + datos["impuesto"], 2),
        "monto_mensual": round(datos["monto"] / datos["duracion_meses"], 2),
        "monto_mensual_con_impuesto": round((datos["monto"] + datos["impuesto"]) / datos["duracion_meses"], 2)
    }
    return datos

def main():
    try:
        args = sys.argv[1:] if len(sys.argv) > 1 else ["--default"]
        if len(args) > 0 and args[0] == "--help":
            print("Uso: python convenio_prestacion_servicios.py [monto_min] [monto_max] [duracion_min] [duracion_max]")
            sys.exit(0)

        monto_min = int(args[0]) if len(args) > 0 else 50000
        monto_max = int(args[1]) if len(args) > 1 else 500000
        duracion_min = int(args[2]) if len(args) > 2 else 3
        duracion_max = int(args[3]) if len(args) > 3 else 24

        convenio = generar_convenio(monto_min, monto_max, duracion_min, duracion_max)

        print("=== CONVENIO DE PRESTACIÓN DE SERVICIOS ===")
        print(f"Número: {convenio['numero_convenio']}")
        print(f"Fecha: {convenio['fecha']}")
        print(f"Monto: ${convenio['monto']:,.2f} MXN")
        print(f"Duración: {convenio['duracion_meses']} meses")
        print(f"Partes: {', '.join(convenio['partes'])}")
        print(f"Impuesto (16%): ${convenio['impuesto']:,.2f} MXN")
        print(f"Total: ${convenio['total']:,.2f} MXN")
        print(f"Monto mensual: ${convenio['monto_mensual']:,.2f} MXN")
        print(f"Monto mensual con impuesto: ${convenio['monto_mensual_con_impuesto']:,.2f} MXN")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Se ha generado un convenio de prestación de servicios con un monto total de ${convenio['total']:,.2f} MXN,")
        print(f"con una duración de {convenio['duracion_meses']} meses y un monto mensual con impuesto de ${convenio['monto_mensual_con_impuesto']:,.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()