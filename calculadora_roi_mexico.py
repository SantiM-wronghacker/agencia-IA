"""
ÁREA: FINANZAS
DESCRIPCIÓN: Calculadora de ROI y flujo de caja neto para propiedades en México
TECNOLOGÍA: Python, sys
"""

import sys
import time

class Propiedad:
    def __init__(self, valor_compra, renta_mensual, gastos_mantenimiento_mensual, predial_anual):
        self.valor_compra = valor_compra
        self.renta_mensual = renta_mensual
        self.gastos_mantenimiento_mensual = gastos_mantenimiento_mensual
        self.predial_anual = predial_anual

    def calcular_roi(self):
        roi_anual = (self.renta_mensual * 12) / self.valor_compra
        return roi_anual

    def calcular_flujo_caja_neto(self):
        flujo_caja_neto_mensual = self.renta_mensual - self.gastos_mantenimiento_mensual
        return flujo_caja_neto_mensual

    def calcular_flujo_caja_neto_anual(self):
        flujo_caja_neto_anual = (self.renta_mensual * 12) - (self.gastos_mantenimiento_mensual * 12) - self.predial_anual
        return flujo_caja_neto_anual


def main():
    print("Calculadora de ROI y flujo de caja neto para propiedades en México")

    if len(sys.argv) == 5:
        valor_compra = float(sys.argv[1])
        renta_mensual = float(sys.argv[2])
        gastos_mantenimiento_mensual = float(sys.argv[3])
        predial_anual = float(sys.argv[4])
    else:
        valor_compra = 2000000.0
        renta_mensual = 15000.0
        gastos_mantenimiento_mensual = 5000.0
        predial_anual = 20000.0
        print(f"Usando valores por defecto: valor_compra={valor_compra}, renta_mensual={renta_mensual}, gastos_mantenimiento_mensual={gastos_mantenimiento_mensual}, predial_anual={predial_anual}")

    propiedad = Propiedad(valor_compra, renta_mensual, gastos_mantenimiento_mensual, predial_anual)

    roi_anual = propiedad.calcular_roi()
    flujo_caja_neto_mensual = propiedad.calcular_flujo_caja_neto()
    flujo_caja_neto_anual = propiedad.calcular_flujo_caja_neto_anual()

    print(f"ROI anual: {roi_anual * 100:.2f}%")
    print(f"Flujo de caja neto mensual: ${flujo_caja_neto_mensual:.2f}")
    print(f"Flujo de caja neto anual: ${flujo_caja_neto_anual:.2f}")


if __name__ == "__main__":
    main()