# LEGAL/Generador de Contrato de Arrendamiento Comercial/Python

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        nombre_arrendador = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez"
        nombre_arrendatario = sys.argv[2] if len(sys.argv) > 2 else "Maria García"
        direccion_inmueble = sys.argv[3] if len(sys.argv) > 3 else "Calle 123, Colonia Centro, Ciudad de México"
        renta_mensual = float(sys.argv[4]) if len(sys.argv) > 4 else 15000.0
        duracion_contrato = int(sys.argv[5]) if len(sys.argv) > 5 else 12

        fecha_inicio = datetime.date.today()
        fecha_fin = fecha_inicio + datetime.timedelta(days=duracion_contrato * 30)

        contrato = {
            "nombre_arrendador": nombre_arrendador,
            "nombre_arrendatario": nombre_arrendatario,
            "direccion_inmueble": direccion_inmueble,
            "renta_mensual": renta_mensual,
            "duracion_contrato": duracion_contrato,
            "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
            "fecha_fin": fecha_fin.strftime("%d/%m/%Y")
        }

        print("Contrato de Arrendamiento Comercial")
        print("------------------------------------")
        print(f"Nombre del Arrendador: {contrato['nombre_arrendador']}")
        print(f"Nombre del Arrendatario: {contrato['nombre_arrendatario']}")
        print(f"Dirección del Inmueble: {contrato['direccion_inmueble']}")
        print(f"Renta Mensual: ${contrato['renta_mensual']:.2f} MXN")
        print(f"Duración del Contrato: {contrato['duracion_contrato']} meses")
        print(f"Fecha de Inicio: {contrato['fecha_inicio']}")
        print(f"Fecha de Fin: {contrato['fecha_fin']}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()