import sys
import json
import datetime
import math

def main():
    try:
        meta = float(sys.argv[1]) if len(sys.argv) > 1 else 100000.0
        ahorro_mensual = float(sys.argv[2]) if len(sys.argv) > 2 else 5000.0
        tasa_interes = float(sys.argv[3]) if len(sys.argv) > 3 else 0.04
        tiempo_ahorro = float(sys.argv[4]) if len(sys.argv) > 4 else 12.0

        monto_total = 0.0
        meses = 0
        while monto_total < meta:
            monto_total += ahorro_mensual
            monto_total += (monto_total * tasa_interes) / 12.0
            meses += 1

        print(f"Meta de ahorro: ${meta:.2f}")
        print(f"Ahorro mensual: ${ahorro_mensual:.2f}")
        print(f"Tasa de interés: {tasa_interes*100:.2f}%")
        print(f"Tiempo de ahorro estimado: {math.ceil(meses)} meses")
        print(f"Monto total ahorrado: ${monto_total:.2f}")
        print(f"Fecha estimada de logro de meta: {(datetime.date.today() + datetime.timedelta(days=math.ceil(meses)*30)).strftime('%d/%m/%Y')}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()