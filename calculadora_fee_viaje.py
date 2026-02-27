# FINANZAS, Calculadora de fee de viaje, Python

import sys
import json
import datetime

def calcula_fee(costo_total):
    fee = costo_total * 0.08
    return fee

def main():
    try:
        costo_total = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        empresa = "Way2TheUnknown"
        dominio = "way2theunknown.com"
        fee = calcula_fee(costo_total)
        print(f"Fecha: {fecha_actual}")
        print(f"Empresa: {empresa}")
        print(f"Dominio: {dominio}")
        print(f"Costo total del viaje: ${costo_total:.2f}")
        print(f"Fee del viaje (8%): ${fee:.2f}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()