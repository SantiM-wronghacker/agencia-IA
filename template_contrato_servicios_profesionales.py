"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza template contrato servicios profesionales
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
from datetime import datetime, timedelta

def generar_contrato():
    # Datos predeterminados
    cliente = "Agencia Santi"
    proveedor = "Consultor Profesional"
    servicios = "Desarrollo de software y consultoría legal"
    fecha_inicio = datetime.now().strftime("%Y-%m-%d")
    fecha_fin = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
    honorarios = 50000.00  # MXN
    retencion = 0.10  # 10%
    iva = 0.16  # 16%

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
"""

    return template

def main():
    try:
        contrato = generar_contrato()
        print(contrato)
        # Guardar en archivo
        with open("contrato_servicios_profesionales.txt", "w", encoding="utf-8") as f:
            f.write(contrato)
        print("\nContrato generado y guardado en 'contrato_servicios_profesionales.txt'")
    except Exception as e:
        print(f"Error al generar el contrato: {e}")

if __name__ == "__main__":
    main()