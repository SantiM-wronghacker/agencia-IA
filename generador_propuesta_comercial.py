"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador propuesta comercial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta
import math

def main():
    try:
        # Parámetros por línea de comandos con defaults
        args = sys.argv[1:]
        if not args:
            args = ["Propuesta_Comercial_2023", "50000", "10", "2023-12-31"]

        nombre_propuesta = args[0]
        monto_inicial = float(args[1])
        meses = int(args[2])
        fecha_limite = args[3]

        # Generar datos de propuesta
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        fecha_entrega = (datetime.now() + timedelta(days=random.randint(1, 15))).strftime("%Y-%m-%d")
        descuento = random.uniform(0.05, 0.20)
        iva = 0.16
        subtotal = monto_inicial * (1 - descuento)
        impuestos = subtotal * iva
        total = subtotal + impuestos

        # Generar datos de contacto
        contactos = [
            {"nombre": "Juan Pérez", "puesto": "Gerente de Compras", "telefono": "5512345678"},
            {"nombre": "María López", "puesto": "Directora de Ventas", "telefono": "5587654321"}
        ]

        # Generar propuesta
        propuesta = {
            "nombre": nombre_propuesta,
            "fecha_creacion": fecha_actual,
            "fecha_entrega": fecha_entrega,
            "monto_inicial": monto_inicial,
            "descuento": descuento,
            "iva": iva,
            "subtotal": subtotal,
            "impuestos": impuestos,
            "total": total,
            "contactos": contactos,
            "condiciones": [
                "Pago al contado 5% de descuento",
                "Pago en 30 días sin descuento",
                "Garantía de 1 año"
            ]
        }

        # Imprimir propuesta
        print(f"Nombre de la propuesta: {propuesta['nombre']}")
        print(f"Fecha de creación: {propuesta['fecha_creacion']}")
        print(f"Fecha de entrega: {propuesta['fecha_entrega']}")
        print(f"Monto inicial: ${propuesta['monto_inicial']:.2f}")
        print(f"Descuento: {propuesta['descuento']*100:.2f}%")
        print(f"Subtotal: ${propuesta['subtotal']:.2f}")
        print(f"Impuestos (16%): ${propuesta['impuestos']:.2f}")
        print(f"Total: ${propuesta['total']:.2f}")
        print("Contactos:")
        for contacto in propuesta['contactos']:
            print(f"  - {contacto['nombre']}: {contacto['puesto']}, Tel. {contacto['telefono']}")
        print("Condiciones:")
        for condicion in propuesta['condiciones']:
            print(f"  - {condicion}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La propuesta {propuesta['nombre']} tiene un monto inicial de ${propuesta['monto_inicial']:.2f} con un descuento de {propuesta['descuento']*100:.2f}%.")
        print(f"El subtotal es de ${propuesta['subtotal']:.2f} y los impuestos son de ${propuesta['impuestos']:.2f}.")
        print(f"El total es de ${propuesta['total']:.2f} y la fecha de entrega es {propuesta['fecha_entrega']}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()