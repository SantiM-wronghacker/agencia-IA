"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza calculadora cac ltv
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto con valores realistas para México
        cac = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0  # CAC en MXN
        ltv = float(sys.argv[2]) if len(sys.argv) > 2 else 1500.0  # LTV en MXN
        meses = int(sys.argv[3]) if len(sys.argv) > 3 else 12  # Periodo en meses
        tasa_descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 10.0  # Tasa de descuento para el cálculo del valor presente

        # Cálculos
        ratio = ltv / cac
        payback_period = cac / (ltv / meses)
        roi = (ltv - cac) / cac * 100
        ltv_anual = ltv * 12 / meses
        margen = ltv - cac
        tasa_recuperacion = (ltv / cac) * 100
        punto_equilibrio = (cac / (ltv - cac)) * 100
        crecimiento_anual = ((ltv_anual - cac) / cac) * 100
        valor_presente = ltv / (1 + tasa_descuento/100)**meses

        # Resultados
        print(f"CAC: ${cac:.2f} MXN")
        print(f"LTV: ${ltv:.2f} MXN")
        print(f"Ratio LTV/CAC: {ratio:.2f}")
        print(f"Payback Period: {payback_period:.1f} meses")
        print(f"ROI: {roi:.1f}%")
        print(f"Margen por cliente: ${margen:.2f} MXN")
        print(f"Tasa de recuperación: {tasa_recuperacion:.1f}%")
        print(f"Punto de equilibrio: {punto_equilibrio:.1f}%")
        print(f"Crecimiento anual: {crecimiento_anual:.1f}%")
        print(f"LTV anual: ${ltv_anual:.2f} MXN")
        print(f"Meses para recuperar la inversión: {payback_period:.1f} meses")
        print(f"Valor presente del LTV: ${valor_presente:.2f} MXN")
        print(f"Tasa de descuento: {tasa_descuento:.1f}%")
        print(f"Período de recuperación de la inversión con descuento: {payback_period * (1 + tasa_descuento/100)**meses:.1f} meses")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La relación LTV/CAC es de {ratio:.2f}, lo que indica que por cada peso invertido en adquisición de clientes, se genera un valor de ${ltv:.2f} MXN.")
        print(f"El período de recuperación de la inversión es de {payback_period:.1f} meses, lo que significa que se recuperará la inversión en un plazo de {payback_period:.1f} meses.")
        print(f"La tasa de crecimiento anual es de {crecimiento_anual:.1f}%, lo que indica un crecimiento significativo en la generación de valor por cliente.")
        print(f"El valor presente del LTV es de ${valor_presente:.2f} MXN, lo que indica el valor actual del LTV considerando la tasa de descuento.")

    except ValueError:
        print("Error: Los parámetros deben ser números.")
    except ZeroDivisionError:
        print("Error: No se puede dividir por cero.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()