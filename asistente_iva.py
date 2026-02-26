"""
ÁREA: FINANZAS
DESCRIPCIÓN: Asistente para calcular el IVA de una lista de montos
TECNOLOGÍA: Python
"""

import sys

class AsistenteIVA:
    def __init__(self, montos, iva=0.16):
        self.montos = montos
        self.iva = iva  

    def calcular_subtotal(self):
        return sum(self.montos)

    def calcular_iva(self):
        return self.calcular_subtotal() * self.iva

    def calcular_total(self):
        return self.calcular_subtotal() + self.calcular_iva()

    def generar_resumen(self):
        subtotal = self.calcular_subtotal()
        iva = self.calcular_iva()
        total = self.calcular_total()

        resumen = f"Resumen de declaración contable:\n"
        resumen += f"Subtotal: ${subtotal:.2f}\n"
        resumen += f"IVA ({self.iva*100}%): ${iva:.2f}\n"
        resumen += f"Total: ${total:.2f}\n"
        resumen += f"Total de montos: {len(self.montos)}\n"
        resumen += f"Monto promedio: ${sum(self.montos)/len(self.montos):.2f}\n"
        resumen += f"Monto máximo: ${max(self.montos):.2f}\n"
        resumen += f"Monto mínimo: ${min(self.montos):.2f}\n"

        return resumen


def main():
    try:
        if len(sys.argv) > 1:
            montos = [float(arg) for arg in sys.argv[1:]]
        else:
            montos = [100, 200, 300, 400, 500]
            print("Usando valores por defecto:", montos)
        asistente = AsistenteIVA(montos)
        print(asistente.generar_resumen())
        print("\nResumen ejecutivo:")
        print("El total a pagar es de ${:.2f}, de los cuales ${:.2f} corresponden a IVA.".format(asistente.calcular_total(), asistente.calcular_iva()))
    except ValueError:
        print("Error: Los argumentos deben ser números.")
    except Exception as e:
        print("Error:", str(e))


if __name__ == "__main__":
    main()