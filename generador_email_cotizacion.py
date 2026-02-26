"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador email cotizacion
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
from datetime import datetime, timedelta
import random

def generar_cotizacion():
    productos = [
        {"nombre": "Laptop HP", "precio": 12999.99, "cantidad": 1},
        {"nombre": "Monitor Dell", "precio": 4999.50, "cantidad": 2},
        {"nombre": "Teclado Logitech", "precio": 899.99, "cantidad": 3},
    ]

    subtotal = sum(item["precio"] * item["cantidad"] for item in productos)
    iva = subtotal * 0.16
    total = subtotal + iva

    return {
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "productos": productos,
        "subtotal": round(subtotal, 2),
        "iva": round(iva, 2),
        "total": round(total, 2),
        "cliente": "Empresa XYZ S.A. de C.V.",
        "vendedor": "Juan Pérez",
        "numero_cotizacion": f"COT-{random.randint(1000, 9999)}"
    }

def generar_email(cotizacion):
    fecha = cotizacion["fecha"]
    productos = "\n".join(
        f"- {item['nombre']}: ${item['precio']:.2f} x {item['cantidad']} = ${item['precio'] * item['cantidad']:.2f}"
        for item in cotizacion["productos"]
    )
    mensaje = f"""
    Estimado/a {cotizacion["cliente"]},

    Adjunto encontrará la cotización {cotizacion["numero_cotizacion"]} con fecha {fecha}.

    Detalle de productos:
    {productos}

    Resumen:
    Subtotal: ${cotizacion["subtotal"]:.2f}
    IVA (16%): ${cotizacion["iva"]:.2f}
    Total: ${cotizacion["total"]:.2f}

    Atentamente,
    {cotizacion["vendedor"]}
    Agencia Santi
    """

    return mensaje

def main():
    try:
        cotizacion = generar_cotizacion()
        email = generar_email(cotizacion)
        print(email)
    except Exception as e:
        print(f"Error al generar la cotización: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()