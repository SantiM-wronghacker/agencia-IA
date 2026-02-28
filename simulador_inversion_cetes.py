"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza simulador de inversión en CETES con cálculos precisos para México
TECNOLOGÍA: Python estándar
"""

import sys
import math
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_intereses(monto, tasa, dias):
    # Cálculo de intereses con redondeo a 4 decimales para mayor precisión
    intereses = monto * (tasa / 365) * dias
    return round(intereses, 4)

def calcular_iva(intereses):
    # Cálculo del IVA sobre intereses (16% en México)
    return intereses * 0.16

def calcular_neto(intereses, iva):
    # Cálculo del monto neto después de impuestos
    return intereses - iva

def main():
    try:
        # Parámetros por defecto
        monto = float(sys.argv[1]) if len(sys.argv) > 1 else 10000.0
        tasa = float(sys.argv[2]) if len(sys.argv) > 2 else 0.07  # 7%
        dias = int(sys.argv[3]) if len(sys.argv) > 3 else 28

        # Validaciones
        if monto <= 0 or tasa <= 0 or dias <= 0:
            print("Error: Valores deben ser positivos")
            return

        if tasa > 1:
            print("Error: Tasa anual debe ser menor o igual a 1 (100%)")
            return

        # Cálculos
        intereses = calcular_intereses(monto, tasa, dias)
        iva = calcular_iva(intereses)
        neto = calcular_neto(intereses, iva)
        total = monto + neto

        # Fecha de vencimiento
        fecha_inicio = datetime.now()
        fecha_vencimiento = fecha_inicio + timedelta(days=dias)

        # Resultados
        print("=== SIMULADOR DE INVERSIÓN EN CETES ===")
        print(f"Monto inicial: ${monto:,.2f} MXN")
        print(f"Tasa anual: {tasa*100:.2f}%")
        print(f"Plazo: {dias} días (hasta {fecha_vencimiento.strftime('%d/%m/%Y')})")
        print(f"Intereses brutos: ${intereses:,.4f} MXN")
        print(f"IVA (16%): ${iva:,.4f} MXN")
        print(f"Intereses netos: ${neto:,.4f} MXN")
        print(f"Monto total al vencimiento: ${total:,.2f} MXN")
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Rendimiento anualizado: {((total/monto) ** (365/dias) - 1)*100:.2f}%")
        print(f"Rendimiento neto anualizado: {((1 + (neto/monto)) ** (365/dias) - 1)*100:.2f}%")
        print(f"Días para duplicar inversión (bruto): {math.log(2)/math.log(1 + (intereses/monto))*(365/dias):.1f} años")
        print(f"Días para duplicar inversión (neto): {math.log(2)/math.log(1 + (neto/monto))*(365/dias):.1f} años")

    except ValueError:
        print("Error: Valores inválidos. Asegúrese de ingresar números válidos.")
    except Exception as e:
        print(f"Error en la simulación: {str(e)}")

if __name__ == "__main__":
    main()