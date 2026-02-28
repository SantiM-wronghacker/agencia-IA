"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza template contrato servicios profesionales
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_contrato(cliente="Agencia Santi", proveedor="Consultor Profesional", servicios="Desarrollo de software y consultoría legal", honorarios=50000.00, retencion=0.10, iva=0.16):
    # Datos predeterminados
    fecha_inicio = datetime.now().strftime("%Y-%m-%d")
    fecha_fin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")

    # Cálculos
    subtotal = honorarios
    retencion_monto = subtotal * retencion
    iva_monto = (subtotal - retencion_monto) * iva
    total = subtotal - retencion_monto + iva_monto

    # Generar template
    template = f"""CONTRATO DE SERVICIOS PROFESIONALES

Entre {cliente}, en lo sucesivo "EL CLIENTE", y {proveedor}, en lo sucesivo "EL PROVEEDOR", se celebra el presente contrato de servicios profesionales, al tenor de las siguientes cláusulas:

1. OBJETO: EL PROVEEDOR se obliga a prestar los siguientes servicios: {servicios}.
2. FECHAS: El contrato tendrá vigencia del {fecha_inicio} al {fecha_fin}.
3. HONORARIOS: La contraprestación será de ${subtotal:,.2f} MXN, con retención del {retencion*100:.0f}% (${retencion_monto:,.2f} MXN) y IVA del {iva*100:.0f}% (${iva_monto:,.2f} MXN), total a pagar: ${total:,.2f} MXN.
4. OBLIGACIONES: EL CLIENTE se obliga a pagar los honorarios en la fecha acordada.
5. TERMINACIÓN: El contrato podrá terminarse por mutuo acuerdo o incumplimiento de cualquiera de las partes.

En señal de conformidad, se firma el presente contrato en la Ciudad de México, a {fecha_inicio}.

{cliente}
________________________
Representante Legal

{proveedor}
________________________
Consultor Profesional

RESUMEN EJECUTIVO:
- Cliente: {cliente}
- Proveedor: {proveedor}
- Servicios: {servicios}
- Fecha de inicio: {fecha_inicio}
- Fecha de fin: {fecha_fin}
- Honorarios: ${subtotal:,.2f} MXN
- Retención: {retencion*100:.0f}%
- IVA: {iva*100:.0f}%
- Total a pagar: ${total:,.2f} MXN
"""

    return template

def main():
    try:
        if len(sys.argv) > 1:
            cliente = sys.argv[1]
            proveedor = sys.argv[2]
            servicios = sys.argv[3]
            honorarios = float(sys.argv[4])
            retencion = float(sys.argv[5])
            iva = float(sys.argv[6])
        else:
            cliente = "Agencia Santi"
            proveedor = "Consultor Profesional"
            servicios = "Desarrollo de software y consultoría legal"
            honorarios = 50000.00
            retencion = 0.10
            iva = 0.16

        contrato = generar_contrato(cliente, proveedor, servicios, honorarios, retencion, iva)
        print(contrato)
        # Guardar en archivo
        with open("contrato.txt", "w") as archivo:
            archivo.write(contrato)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()