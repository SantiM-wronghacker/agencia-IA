"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza plan comercializacion propiedad
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Parámetros por defecto
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 5000000.0
        comision_agente = float(sys.argv[2]) if len(sys.argv) > 2 else 0.05
        gastos_cierre = float(sys.argv[3]) if len(sys.argv) > 3 else 0.10
        impuesto_traslado = float(sys.argv[4]) if len(sys.argv) > 4 else 0.02
        impuesto_over = float(sys.argv[5]) if len(sys.argv) > 5 else 0.08
        tasa_interes_anual = float(sys.argv[6]) if len(sys.argv) > 6 else 0.12

        # Cálculo de comisiones y gastos
        comision_agente_total = precio_venta * comision_agente
        gastos_cierre_total = precio_venta * gastos_cierre
        impuesto_traslado_total = precio_venta * impuesto_traslado
        impuesto_over_total = precio_venta * impuesto_over
        tasa_interes_mensual = (tasa_interes_anual / 12) * precio_venta

        # Resumen de resultados
        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Comisión del agente: ${comision_agente_total:,.2f} MXN ({comision_agente*100:.2f}%)")
        print(f"Gastos de cierre: ${gastos_cierre_total:,.2f} MXN ({gastos_cierre*100:.2f}%)")
        print(f"Impuesto de traslado: ${impuesto_traslado_total:,.2f} MXN ({impuesto_traslado*100:.2f}%)")
        print(f"Impuesto sobre la renta: ${impuesto_over_total:,.2f} MXN ({impuesto_over*100:.2f}%)")
        print(f"Tasa de interés mensual: ${tasa_interes_mensual:,.2f} MXN")
        print(f"Total a pagar: ${precio_venta + comision_agente_total + gastos_cierre_total + impuesto_traslado_total + impuesto_over_total:,.2f} MXN")
        print(f"Total a pagar con intereses: ${precio_venta + comision_agente_total + gastos_cierre_total + impuesto_traslado_total + impuesto_over_total + tasa_interes_mensual:,.2f} MXN")
        print(f"Fecha de cálculo: {datetime.date.today()}")
        print(f"Moneda: MXN (Pesos Mexicanos)")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El precio de venta de la propiedad es de ${precio_venta:,.2f} MXN.")
        print(f"El total a pagar, incluyendo comisiones y gastos, es de ${precio_venta + comision_agente_total + gastos_cierre_total + impuesto_traslado_total + impuesto_over_total:,.2f} MXN.")
        print(f"El total a pagar con intereses es de ${precio_venta + comision_agente_total + gastos_cierre_total + impuesto_traslado_total + impuesto_over_total + tasa_interes_mensual:,.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: No se proporcionaron los parámetros necesarios.")
    except ValueError:
        print("Error: Los parámetros proporcionados no son válidos.")

if __name__ == "__main__":
    main()