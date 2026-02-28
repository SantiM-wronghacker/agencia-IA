import sys
import json
import datetime
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parametros por defecto
        años = 3
        ingresos_anuales = 1000000  # Ingresos anuales promedio de una empresa en México
        gastos_anuales = 500000  # Gastos anuales promedio de una empresa en México
        tasa_interes = 0.05  # Tasa de interés promedio en México

        # Verificar parámetros por línea de comandos
        if len(sys.argv) > 1:
            try:
                años = int(sys.argv[1])
                ingresos_anuales = float(sys.argv[2])
                gastos_anuales = float(sys.argv[3])
                tasa_interes = float(sys.argv[4])
            except ValueError:
                print("Error: Parámetros inválidos. Utilice: python proyector_flujo_caja_3_anos.py <años> <ingresos_anuales> <gastos_anuales> <tasa_interes>")
                return

        # Calculo de flujo de caja
        flujo_caja = []
        for año in range(años):
            ingresos = ingresos_anuales * (1 + (año * 0.1))  # Aumento del 10% anual en ingresos
            gastos = gastos_anuales * (1 + (año * 0.05))  # Aumento del 5% anual en gastos
            flujo = ingresos - gastos
            flujo_caja.append({
                "año": año + 1,
                "ingresos": round(ingresos, 2),
                "gastos": round(gastos, 2),
                "flujo": round(flujo, 2)
            })

        # Calculo de intereses
        intereses = []
        saldo = 0
        for año in range(años):
            saldo += flujo_caja[año]["flujo"]
            interes = saldo * tasa_interes
            intereses.append({
                "año": año + 1,
                "saldo": round(saldo, 2),
                "interes": round(interes, 2)
            })

        # Imprimir resultados
        print(f"Proyección de flujo de caja para {años} años:")
        for flujo in flujo_caja:
            print(f"Año {flujo['año']}: Ingresos ${flujo['ingresos']}, Gastos ${flujo['gastos']}, Flujo ${flujo['flujo']}")
        print("\nProyección de intereses:")
        for interes in intereses:
            print(f"Año {interes['año']}: Saldo ${interes['saldo']}, Interés ${interes['interes']}")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Flujo de caja total: ${round(sum([flujo['flujo'] for flujo in flujo_caja]), 2)}")
        print(f"Interés total: ${round(sum([interes['interes'] for interes in intereses]), 2)}")
        print(f"Saldo final: ${round(intereses[-1]['saldo'], 2)}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()