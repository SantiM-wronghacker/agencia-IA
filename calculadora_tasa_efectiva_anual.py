# FINANZAS / Calculadora de tasa efectiva anual / Python

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_tasa_efectiva_anual(tasa_nominal, frecuencia):
    return (1 + (tasa_nominal / 100) / frecuencia) ** frecuencia - 1

def main():
    try:
        tasa_nominal = float(sys.argv[1]) if len(sys.argv) > 1 else 10.0
        frecuencia = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        capital = float(sys.argv[3]) if len(sys.argv) > 3 else 10000.0
        años = int(sys.argv[4]) if len(sys.argv) > 4 else 1
        tasa_efectiva_anual = calcula_tasa_efectiva_anual(tasa_nominal, frecuencia)
        print(f"Tasa nominal: {tasa_nominal}%")
        print(f"Frecuencia de pago: {frecuencia} veces al año")
        print(f"Tasa efectiva anual: {tasa_efectiva_anual * 100:.4f}%")
        print(f"Interés anual: {(tasa_efectiva_anual * 100):.4f}%")
        print(f"Ejemplo con ${capital:.2f}: ${capital * (1 + tasa_efectiva_anual):.2f}")
        print(f"Interés generado: ${capital * tasa_efectiva_anual:.2f}")
        print(f"Tiempo para duplicar la inversión: {math.log(2) / math.log(1 + tasa_efectiva_anual):.2f} años")
        print(f"Valor presente de una anualidad de ${capital:.2f} durante {años} años: ${capital / (1 + tasa_efectiva_anual)**años:.2f}")
        print(f"Valor futuro de una anualidad de ${capital:.2f} durante {años} años: ${capital * (1 + tasa_efectiva_anual)**años:.2f}")
        print(f"Interés total generado en {años} años: ${capital * ((1 + tasa_efectiva_anual)**años - 1):.2f}")
        print(f"Cuota anual para pagar un préstamo de ${capital:.2f} en {años} años: ${capital * tasa_efectiva_anual / (1 - (1 + tasa_efectiva_anual)**(-años)):.2f}")
        print(f"Cuota mensual para pagar un préstamo de ${capital:.2f} en {años} años: ${capital * tasa_efectiva_anual / (1 - (1 + tasa_efectiva_anual)**(-años)) / 12:.2f}")
        print("Resumen ejecutivo:")
        print(f"La tasa efectiva anual es {tasa_efectiva_anual * 100:.4f}%")
        print(f"El interés anual es {(tasa_efectiva_anual * 100):.4f}%")
        print(f"El valor futuro de la inversión es ${capital * (1 + tasa_efectiva_anual):.2f}")
        print(f"El interés total generado en {años} años es ${capital * ((1 + tasa_efectiva_anual)**años - 1):.2f}")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except ZeroDivisionError as e:
        print(f"Error de división por cero: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()