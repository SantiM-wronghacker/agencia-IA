# FRANQUICIAS / Calculadora de Regalias Franquicia / Python
import sys
import json
import datetime
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_regalias(ventas, porcentaje_regalia, iva=0.16, isr=0.1):
    regalia = ventas * porcentaje_regalia / 100
    iva_regalia = regalia * iva
    isr_regalia = regalia * isr
    total_regalia = regalia + iva_regalia + isr_regalia
    return regalia, iva_regalia, isr_regalia, total_regalia

def main():
    try:
        ventas = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        porcentaje_regalia = float(sys.argv[2]) if len(sys.argv) > 2 else 5.0
        iva = float(sys.argv[3]) if len(sys.argv) > 3 else 0.16
        isr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
        regalia, iva_regalia, isr_regalia, total_regalia = calcular_regalias(ventas, porcentaje_regalia, iva, isr)
        print(f"Fecha de calculo: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Ventas: ${ventas:,.2f} MXN")
        print(f"Porcentaje de regalia: {porcentaje_regalia}%")
        print(f"Regalia: ${regalia:,.2f} MXN")
        print(f"IVA ({iva*100}%): ${iva_regalia:,.2f} MXN")
        print(f"ISR ({isr*100}%): ${isr_regalia:,.2f} MXN")
        print(f"Total de regalia: ${total_regalia:,.2f} MXN")
        print(f"Total a pagar: ${ventas - total_regalia:,.2f} MXN")
        print(f"Utilidad: ${ventas - total_regalia:,.2f} MXN")
        print(f"Margen de utilidad: {(ventas - total_regalia) / ventas * 100:.2f}%")
        print(f"Margen de regalia: {(total_regalia) / ventas * 100:.2f}%")
        print(f"Margen de IVA: {(iva_regalia) / ventas * 100:.2f}%")
        print(f"Margen de ISR: {(isr_regalia) / ventas * 100:.2f}%")
        print("Resumen Ejecutivo:")
        print(f"La regalia total asciende a ${total_regalia:,.2f} MXN, lo que representa {porcentaje_regalia}% de las ventas.")
        print(f"El total a pagar es de ${ventas - total_regalia:,.2f} MXN, con una utilidad de ${ventas - total_regalia:,.2f} MXN.")
        print(f"La regalia representa {total_regalia / ventas * 100:.2f}% de las ventas, mientras que el IVA y el ISR representan {iva_regalia / ventas * 100:.2f}% y {isr_regalia / ventas * 100:.2f}% respectivamente.")
    except Exception as e:
        print(f"Error: {str(e)}")
    except ValueError:
        print("Error: Los valores ingresados deben ser numericos.")
    except IndexError:
        print("Error: Debe ingresar los valores de ventas, porcentaje de regalia, IVA y ISR.")

if __name__ == '__main__':
    main()