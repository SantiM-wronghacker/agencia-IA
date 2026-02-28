"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza calculadora roi educativo
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
        # Parámetros por defecto
        inversion = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        porcentaje_interes = float(sys.argv[2]) if len(sys.argv) > 2 else 6.0  # Tasa de interés promedio en México
        años = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        tasa_inflacion = float(sys.argv[4]) if len(sys.argv) > 4 else 3.5  # Tasa de inflación promedio en México

        # Cálculo del ROI
        roi = (inversion * (1 + porcentaje_interes / 100) ** años) - inversion

        # Cálculo del ROI anual
        roi_anual = (inversion * (1 + porcentaje_interes / 100)) - inversion

        # Cálculo del valor presente neto
        vpn = inversion * ((1 + porcentaje_interes / 100) ** años) / (1 + tasa_inflacion / 100) ** años - inversion

        # Cálculo de la tasa interna de retorno
        tir = ((inversion * (1 + porcentaje_interes / 100) ** años) / inversion) ** (1 / años) - 1

        # Impresión de resultados
        print(f"Inversión inicial: ${inversion:,.2f} MXN")
        print(f"Interés anual: {porcentaje_interes}%")
        print(f"Años: {años}")
        print(f"Tasa de inflación: {tasa_inflacion}%")
        print(f"ROI total: ${roi:,.2f} MXN")
        print(f"ROI anual: ${roi_anual:,.2f} MXN")
        print(f"Valor presente neto: ${vpn:,.2f} MXN")
        print(f"Tasa interna de retorno: {tir * 100:.2f}%")

        # Resumen ejecutivo
        print("\nResumen ejecutivo:")
        print(f"La inversión de ${inversion:,.2f} MXN durante {años} años con un interés anual de {porcentaje_interes}% y una tasa de inflación de {tasa_inflacion}% generará un ROI total de ${roi:,.2f} MXN y un ROI anual de ${roi_anual:,.2f} MXN.")
        print(f"El valor presente neto de la inversión es de ${vpn:,.2f} MXN y la tasa interna de retorno es de {tir * 100:.2f}%.")

        # Conclusión
        print("\nConclusión:")
        if roi > 0:
            print(f"La inversión es rentable, con un ROI total de ${roi:,.2f} MXN.")
        else:
            print(f"La inversión no es rentable, con un ROI total de ${roi:,.2f} MXN.")

    except Exception as e:
        print(f"Error: {str(e)}")
    except IndexError:
        print("Error: No se han proporcionado suficientes parámetros. Por favor, proporcione los siguientes parámetros: inversion, porcentaje_interes, años, tasa_inflacion")

if __name__ == "__main__":
    main()