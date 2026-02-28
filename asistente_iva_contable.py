"""
ÁREA: FINANZAS
DESCRIPCIÓN: Asistente para calcular IVA y subtotal de montos
TECNOLOGÍA: Python
"""

import sys
import time
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class AsistenteIVAContable:
    def __init__(self, montos, iva_porcentaje=0.16):
        self.montos = montos
        self.iva_porcentaje = iva_porcentaje

    def separar_iva(self):
        iva_total = 0
        subtotal_total = 0
        resumen = []

        for monto in self.montos:
            try:
                iva = monto * self.iva_porcentaje
                subtotal = monto / (1 + self.iva_porcentaje)

                iva_total += iva
                subtotal_total += subtotal

                resumen.append({
                    'monto': monto,
                    'iva': iva,
                    'subtotal': subtotal
                })
            except ZeroDivisionError:
                print("Error: No se puede dividir por cero.")
                return None, None, None
            except TypeError:
                print("Error: El monto debe ser un número.")
                return None, None, None

        return resumen, iva_total, subtotal_total

    def generar_resumen(self):
        resumen, iva_total, subtotal_total = self.separar_iva()

        if resumen is None:
            return

        print("Resumen de Montos:")
        for i, item in enumerate(resumen):
            print(f"Monto {i+1}: {item['monto']:.2f}, IVA: {item['iva']:.2f}, Subtotal: {item['subtotal']:.2f}")

        print("\nTotales:")
        print(f"Total de Montos: {sum(self.montos):.2f}")
        print(f"Total de IVA: {iva_total:.2f}")
        print(f"Total de Subtotales: {subtotal_total:.2f}")
        print(f"Promedio de Montos: {sum(self.montos) / len(self.montos):.2f}")
        print(f"Mayor Monto: {max(self.montos):.2f}")
        print(f"Menor Monto: {min(self.montos):.2f}")

        print("\nResumen Ejecutivo:")
        print(f"El total de montos es de {sum(self.montos):.2f}, con un IVA total de {iva_total:.2f} y un subtotal total de {subtotal_total:.2f}.")
        print(f"El promedio de montos es de {sum(self.montos) / len(self.montos):.2f}, con un mayor monto de {max(self.montos):.2f} y un menor monto de {min(self.montos):.2f}.")

def main():
    if len(sys.argv) > 1:
        try:
            montos = [float(arg) for arg in sys.argv[1:]]
        except ValueError:
            print("Error: Los montos deben ser números.")
            return
    else:
        montos = [100, 200, 300, 400, 500]
        print("Usando montos por defecto:", montos)

    asistente = AsistenteIVAContable(montos)
    asistente.generar_resumen()

if __name__ == "__main__":
    main()