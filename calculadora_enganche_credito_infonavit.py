# REAL ESTATE / Calculadora de Enganche de Credito Infonavit / Python

import sys
import json
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_enganche(sueldo, antiguedad, precio_casa):
    enganche = 0
    if sueldo <= 10000:
        enganche = precio_casa * 0.1
    elif sueldo <= 20000:
        enganche = precio_casa * 0.12
    else:
        enganche = precio_casa * 0.15
    if antiguedad >= 5:
        enganche *= 0.9
    return enganche

def main():
    try:
        sueldo = float(sys.argv[1]) if len(sys.argv) > 1 else 15000
        antiguedad = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        precio_casa = float(sys.argv[3]) if len(sys.argv) > 3 else 500000
        tasa_interes = float(sys.argv[4]) if len(sys.argv) > 4 else 0.07
        plazo_credito = int(sys.argv[5]) if len(sys.argv) > 5 else 20
        enganche = calcula_enganche(sueldo, antiguedad, precio_casa)
        credito_infonavit = precio_casa - enganche
        cuota_mensual = credito_infonavit * (tasa_interes / 12) * (1 + tasa_interes / 12) ** (plazo_credito * 12) / ((1 + tasa_interes / 12) ** (plazo_credito * 12) - 1)
        total_a_pagar = credito_infonavit + (credito_infonavit * tasa_interes * plazo_credito)
        print(f"Sueldo: ${sueldo:.2f}")
        print(f"Antigüedad: {antiguedad} años")
        print(f"Precio de la casa: ${precio_casa:.2f}")
        print(f"Enganche: ${enganche:.2f}")
        print(f"Crédito Infonavit: ${credito_infonavit:.2f}")
        print(f"Tasa de interés: {tasa_interes * 100}%")
        print(f"Plazo de crédito: {plazo_credito} años")
        print(f"Cuota mensual: ${cuota_mensual:.2f}")
        print(f"Total a pagar: ${total_a_pagar:.2f}")
        print(f"Intereses totales: ${total_a_pagar - credito_infonavit:.2f}")
        print(f"Cuotas totales: {plazo_credito * 12}")
        print(f"Fecha de inicio del crédito: {datetime.date.today()}")
        print(f"Fecha de fin del crédito: {(datetime.date.today() + datetime.timedelta(days=plazo_credito*365))}")
        print("Resumen ejecutivo:")
        print(f"Para un sueldo de ${sueldo:.2f} y una antigüedad de {antiguedad} años, el enganche para una casa de ${precio_casa:.2f} es de ${enganche:.2f}.")
        print(f"El crédito Infonavit sería de ${credito_infonavit:.2f} con una tasa de interés de {tasa_interes * 100}% y un plazo de {plazo_credito} años.")
        print(f"La cuota mensual sería de ${cuota_mensual:.2f} y el total a pagar sería de ${total_a_pagar:.2f}.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    import datetime
    main()