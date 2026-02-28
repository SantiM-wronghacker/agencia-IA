"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza generador factura conceptos
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_factura_conceptos(rfc_emisor, rfc_receptor, conceptos):
    try:
        # Datos base
        fecha = datetime.now().strftime("%Y-%m-%d")

        # Validar RFC
        if not validar_rfc(rfc_emisor) or not validar_rfc(rfc_receptor):
            raise ValueError("RFC inválido")

        # Validar conceptos
        if not conceptos:
            raise ValueError("No se han proporcionado conceptos")

        # Generar subtotal
        subtotal = sum(concepto["cantidad"] * concepto["precio"] for concepto in conceptos)
        iva = subtotal * 0.16
        total = subtotal + iva

        # Crear factura
        factura = {
            "fecha": fecha,
            "rfc_emisor": rfc_emisor,
            "rfc_receptor": rfc_receptor,
            "conceptos": conceptos,
            "subtotal": round(subtotal, 2),
            "iva": round(iva, 2),
            "total": round(total, 2)
        }

        return factura
    except Exception as e:
        raise ValueError(f"Error al generar factura: {str(e)}")

def validar_rfc(rfc):
    # Validar formato de RFC
    if len(rfc) != 13:
        return False
    if not rfc[:2].isalpha() or not rfc[2:12].isdigit() or not rfc[12].isalpha():
        return False
    return True

def main():
    try:
        if len(sys.argv) != 3:
            print("Uso: python generador_factura_conceptos.py <rfc_emisor> <rfc_receptor>", file=sys.stderr)
            sys.exit(1)

        rfc_emisor = sys.argv[1]
        rfc_receptor = sys.argv[2]

        conceptos = [
            {"clave": "01", "descripcion": "Consultoría en sistemas", "cantidad": 5, "precio": 1200.50},
            {"clave": "02", "descripcion": "Desarrollo de software", "cantidad": 3, "precio": 2500.75},
            {"clave": "03", "descripcion": "Mantenimiento preventivo", "cantidad": 2, "precio": 800.25},
            {"clave": "04", "descripcion": "Capacitación en Python", "cantidad": 1, "precio": 3000.00},
            {"clave": "05", "descripcion": "Soporte técnico", "cantidad": 4, "precio": 600.00}
        ]

        factura = generar_factura_conceptos(rfc_emisor, rfc_receptor, conceptos)
        print(json.dumps(factura, indent=2, ensure_ascii=False))

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Fecha: {factura['fecha']}")
        print(f"RFC Emisor: {factura['rfc_emisor']}")
        print(f"RFC Receptor: {factura['rfc_receptor']}")
        print(f"Total: ${factura['total']:.2f}")
        print(f"Subtotal: ${factura['subtotal']:.2f}")
        print(f"IVA: ${factura['iva']:.2f}")
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()