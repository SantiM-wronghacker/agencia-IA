"""
ÁREA: CONTABILIDAD
DESCRIPCIÓN: Agente que realiza generador balance general simple
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime
import math

def main():
    try:
        # Parámetros por defecto
        fecha = datetime.now().strftime("%Y-%m-%d")
        activos = 1500000.00
        pasivos = 800000.00
        capital = 700000.00
        impuestos = 0.16
        depreciacion = 0.05

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                fecha = sys.argv[1]
                activos = float(sys.argv[2]) if len(sys.argv) > 2 else activos
                pasivos = float(sys.argv[3]) if len(sys.argv) > 3 else pasivos
                capital = float(sys.argv[4]) if len(sys.argv) > 4 else capital
                impuestos = float(sys.argv[5]) if len(sys.argv) > 5 else impuestos
                depreciacion = float(sys.argv[6]) if len(sys.argv) > 6 else depreciacion
            except (ValueError, IndexError):
                pass

        # Generar balance general
        balance = {
            "fecha": fecha,
            "activos": activos,
            "pasivos": pasivos,
            "capital": capital,
            "total": activos,
            "impuestos": activos * impuestos,
            "depreciacion": activos * depreciacion,
            "utilidad_neta": activos - pasivos - (activos * impuestos) - (activos * depreciacion)
        }

        # Validar ecuación contable
        if not math.isclose(balance["activos"], balance["pasivos"] + balance["capital"], rel_tol=1e-9):
            raise ValueError("Error: La ecuación contable no se cumple")

        # Imprimir balance
        print("BALANCE GENERAL SIMPLE")
        print(f"Fecha: {balance['fecha']}")
        print(f"Activos: ${balance['activos']:,.2f} MXN")
        print(f"Pasivos: ${balance['pasivos']:,.2f} MXN")
        print(f"Capital: ${balance['capital']:,.2f} MXN")
        print(f"Total: ${balance['total']:,.2f} MXN")
        print(f"Impuestos: ${balance['impuestos']:,.2f} MXN")
        print(f"Depreciación: ${balance['depreciacion']:,.2f} MXN")
        print(f"Utilidad Neta: ${balance['utilidad_neta']:,.2f} MXN")
        print(f"Rozamiento: {(balance['activos'] - balance['pasivos'] - balance['capital']) * 100 / balance['activos']:,.2f}%")
        print(f"Margen de utilidad: {(balance['utilidad_neta'] / balance['activos']) * 100:,.2f}%")

        # Resumen ejecutivo
        print("\nRESUMEN EJECUTIVO")
        print(f"La situación financiera de la empresa es estable, con un activo total de ${balance['activos']:,.2f} MXN y un pasivo total de ${balance['pasivos']:,.2f} MXN.")
        print(f"La utilidad neta es de ${balance['utilidad_neta']:,.2f} MXN, lo que representa un margen de utilidad del {(balance['utilidad_neta'] / balance['activos']) * 100:,.2f}%.")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()