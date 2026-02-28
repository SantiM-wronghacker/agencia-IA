import sys
import json
import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# ARCHIVO: simulador_ahorro_meta_personal.py
# AREA: FINANZAS PERSONALES
# DESCRIPCION: Agente que realiza simulador ahorro meta personal
# TECNOLOGIA: Python

def main():
    try:
        meta = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        ahorro_mensual = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 0.04
        tiempo_ahorro = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0

        monto_total = 0.0
        meses = 0
        intereses_ganados = 0.0
        while monto_total < meta:
            monto_total += ahorro_mensual
            interes_mensual = (monto_total * tasa_interes) / 12.0
            monto_total += interes_mensual
            intereses_ganados += interes_mensual
            meses += 1

        print(f"Meta de ahorro: ${meta:.2f}")
        print(f"Ahorro mensual: ${ahorro_mensual:.2f}")
        print(f"Tasa de interés: {tasa_interes*100:.2f}%")
        print(f"Tiempo de ahorro estimado: {math.ceil(meses)} meses")
        print(f"Monto total ahorrado: ${monto_total:.2f}")
        print(f"Intereses ganados: ${intereses_ganados:.2f}")
        print(f"Fecha estimada de logro de meta: {(datetime.date.today() + datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}")
        print(f"Total de ahorro mensual realizado: ${ahorro_mensual * math.ceil(meses):.2f}")
        print(f"Porcentaje de intereses ganados sobre el monto total: {(intereses_ganados / monto_total) * 100 if monto_total > 0 else 0:.2f}%")
        print(f"Resumen Ejecutivo: La meta de ahorro de ${meta:.2f} se logrará en {math.ceil(meses)} meses, con un total de ${monto_total:.2f} ahorrados, incluyendo ${intereses_ganados:.2f} en intereses ganados.")
        print(f"Detalle de ahorro mensual:")
        for i in range(math.ceil(meses)):
            monto_mensual = ahorro_mensual + (ahorro_mensual * tasa_interes) / 12.0
            print(f"Mes {i+1}: ${monto_mensual:.2f}")
        print(f"Proyección de intereses ganados anuales: ${intereses_ganados * 12 / meses:.2f}")
        print(f"Porcentaje de crecimiento anual del ahorro: {(monto_total / ahorro_mensual) * 100 / meses:.2f}%")
        print(f"Tiempo estimado para duplicar el ahorro: {math.log(2) / (tasa_interes / 12.0):.2f} meses")
    except ValueError as e:
        print(f"Error: {str(e)} - Por favor, ingrese valores numéricos válidos.")
    except IndexError as e:
        print(f"Error: {str(e)} - Por favor, ingrese todos los parámetros necesarios.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()