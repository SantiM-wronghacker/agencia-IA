"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza calculadora cac ltv
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        # Parámetros por defecto con valores realistas para México
        cac = float(sys.argv[1]) if len(sys.argv) > 1 else 500.0  # CAC en MXN
        ltv = float(sys.argv[2]) if len(sys.argv) > 2 else 1500.0  # LTV en MXN
        meses = int(sys.argv[3]) if len(sys.argv) > 3 else 12  # Periodo en meses

        # Cálculos
        ratio = ltv / cac
        payback_period = cac / (ltv / meses)
        roi = (ltv - cac) / cac * 100
        ltv_anual = ltv * 12 / meses
        margen = ltv - cac
        tasa_recuperacion = (ltv / cac) * 100
        punto_equilibrio = (cac / (ltv - cac)) * 100
        crecimiento_anual = ((ltv_anual - cac) / cac) * 100

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

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La relación LTV/CAC es de {ratio:.2f}, lo que indica que por cada peso invertido en adquisición de clientes, se genera un valor de ${ltv:.2f} MXN.")
        print(f"El período de recuperación de la inversión es de {payback_period:.1f} meses, lo que significa que se recuperará la inversión en un plazo de {payback_period:.1f} meses.")
        print(f"La tasa de crecimiento anual es de {crecimiento_anual:.1f}%, lo que indica un crecimiento significativo en la generación de valor por cliente.")

    except (ValueError, IndexError, ZeroDivisionError) as e:
        print("Error en los parámetros de entrada. Usando valores por defecto.")
        print("Uso: python calculadora_cac_ltv.py <CAC> <LTV> <meses>")
        main()  # Reinicia con valores por defecto

    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()