"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza checklist requisitos notariales
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        tipo_tramite = sys.argv[1] if len(sys.argv) > 1 else "compra_venta"
        valor_operacion = float(sys.argv[2]) if len(sys.argv) > 2 else 1500000.0
        estado = sys.argv[3] if len(sys.argv) > 3 else "CDMX"

        # Requisitos base
        requisitos = {
            "identificacion": ["INE vigente", "Comprobante de domicilio (no mayor a 3 meses)"],
            "documentos_propiedad": ["Escrituras públicas", "Avalúo catastral actualizado"],
            "pagos": [
                f"ISR (1.5% de ${valor_operacion * 0.015:.2f})",
                f"Derechos notariales (${valor_operacion * 0.005:.2f})",
                f"Impuesto predial (${valor_operacion * 0.002:.2f})"
            ],
            "fechas": {
                "ultimo_pago_predial": datetime.now().strftime("%Y-%m-%d"),
                "ultimo_avaluo": datetime.now().strftime("%Y-%m-%d")
            }
        }

        # Requisitos adicionales por tipo de trámite
        if tipo_tramite == "herencia":
            requisitos["documentos_propiedad"].append("Testamento público")
            requisitos["pagos"].append("Derechos de sucesión (1% de ${:.2f})".format(valor_operacion * 0.01))

        # Requisitos por estado
        if estado == "Jalisco":
            requisitos["pagos"].append("Derechos estatales (${:.2f})".format(valor_operacion * 0.003))

        # Impresión de resultados
        print("CHECKLIST REQUISITOS NOTARIALES")
        print("=" * 40)
        print(f"Tipo de trámite: {tipo_tramite.upper()}")
        print(f"Valor de operación: ${valor_operacion:,.2f} MXN")
        print(f"Estado: {estado.upper()}")
        print("\nREQUISITOS:")
        for categoria, items in requisitos.items():
            print(f"\n{categoria.upper()}:")
            if isinstance(items, dict):
                for k, v in items.items():
                    print(f"  - {k}: {v}")
            else:
                for item in items:
                    print(f"  - {item}")

    except Exception as e:
        print(f"Error en el proceso: {str(e)}")

if __name__ == "__main__":
    main()