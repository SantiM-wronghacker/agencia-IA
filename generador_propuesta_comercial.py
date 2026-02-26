"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador propuesta comercial
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

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
        total = monto_inicial * (1 - descuento) * (1 + iva)

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
            "total": total,
            "contactos": contactos,
            "condiciones": [
                "Pago al contado 5% de descuento",
                "Pago en 30 días sin descuento",
                "Garantía de 1 año"
            ]
        }

        # Mostrar propuesta
        print("Propuesta Comercial Generada")
        print(f"Nombre: {propuesta['nombre']}")
        print(f"Fecha de Entrega: {propuesta['fecha_entrega']}")
        print(f"Monto Total: ${propuesta['total']:,.2f} MXN")
        print(f"Descuento Aplicado: {propuesta['descuento']*100:.1f}%")
        print(f"Contacto Principal: {propuesta['contactos'][0]['nombre']} - {propuesta['contactos'][0]['puesto']}")

        # Guardar en archivo JSON
        with open(f"{propuesta['nombre']}.json", "w") as f:
            json.dump(propuesta, f, indent=4)

    except Exception as e:
        print(f"Error al generar propuesta: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()