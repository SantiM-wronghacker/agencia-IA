# FINANZAS, Calculadora de fee de viaje, Python
# AREA: FINANZAS
# DESCRIPCION: Calcula el 8% de fee sobre costo total
# TECNOLOGIA: Python

import sys
import json
import datetime
import math

def calcula_fee(costo_total, tasa_fee=0.08):
    fee = costo_total * tasa_fee
    return fee

def calcula_iva(costo_total, tasa_iva=0.16):
    iva = costo_total * tasa_iva
    return iva

def calcula_isr(costo_total, tasa_isr=0.1):
    isr = costo_total * tasa_isr
    return isr

def main():
    try:
        costo_total = float(sys.argv[1]) if len(sys.argv) > 1 else 1000.0
        tasa_fee = float(sys.argv[2]) if len(sys.argv) > 2 else 0.08
        tasa_iva = float(sys.argv[3]) if len(sys.argv) > 3 else 0.16
        tasa_isr = float(sys.argv[4]) if len(sys.argv) > 4 else 0.1
        fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        empresa = sys.argv[5] if len(sys.argv) > 5 else "Way2TheUnknown"
        dominio = sys.argv[6] if len(sys.argv) > 6 else "way2theunknown.com"
        fee = calcula_fee(costo_total, tasa_fee)
        iva = calcula_iva(costo_total, tasa_iva)
        isr = calcula_isr(costo_total, tasa_isr)
        total_con_fee_iva_isr = costo_total + fee + iva + isr
        print(f"Fecha: {fecha_actual}")
        print(f"Empresa: {empresa}")
        print(f"Dominio: {dominio}")
        print(f"Costo total del viaje: ${costo_total:.2f}")
        print(f"Fee del viaje ({tasa_fee*100}%): ${fee:.2f}")
        print(f"IVA del viaje ({tasa_iva*100}%): ${iva:.2f}")
        print(f"ISR del viaje ({tasa_isr*100}%): ${isr:.2f}")
        print(f"Total con fee e IVA e ISR: ${total_con_fee_iva_isr:.2f}")
        print(f"Resumen ejecutivo: El costo total del viaje es de ${costo_total:.2f}, con un fee de ${fee:.2f}, un IVA de ${iva:.2f} y un ISR de ${isr:.2f}, para un total de ${total_con_fee_iva_isr:.2f}")
        print(f"Detalles del viaje:")
        print(f"  - Costo total: ${costo_total:.2f}")
        print(f"  - Fee: ${fee:.2f} ({tasa_fee*100}%)")
        print(f"  - IVA: ${iva:.2f} ({tasa_iva*100}%)")
        print(f"  - ISR: ${isr:.2f} ({tasa_isr*100}%)")
        print(f"  - Total con fee e IVA e ISR: ${total_con_fee_iva_isr:.2f}")
        print(f"  - Porcentaje de fee sobre el costo total: {tasa_fee*100}%")
        print(f"  - Porcentaje de IVA sobre el costo total: {tasa_iva*100}%")
        print(f"  - Porcentaje de ISR sobre el costo total: {tasa_isr*100}%")
        print(f"Resumen final:")
        print(f"  - Costo total del viaje: ${costo_total:.2f}")
        print(f"  - Total con fee e IVA e ISR: ${total_con_fee_iva_isr:.2f}")
        print(f"  - Diferencia entre el total con fee e IVA e ISR y el costo total: ${total_con_fee_iva_isr - costo_total:.2f}")
    except ValueError:
        print("Error: Los argumentos deben ser números.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()