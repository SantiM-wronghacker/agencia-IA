"""
ÁREA: FINANZAS
DESCRIPCIÓN: Simulador de utilidades para calcular utilidades anuales y mensuales
TECNOLOGÍA: Python
"""

import sys
import time

class SimuladorUtilidades:
    def __init__(self, metas_ventas_mensuales, gastos_fijos_mensuales):
        self.metas_ventas_mensuales = metas_ventas_mensuales
        self.gastos_fijos_mensuales = gastos_fijos_mensuales

    def calcular_utilidades_anuales(self):
        utilidades_anuales = 0
        for i in range(12):
            utilidad_mensual = self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]
            utilidades_anuales += utilidad_mensual
        return utilidades_anuales

    def calcular_utilidad_mensual(self, mes):
        if mes < 1 or mes > 12:
            raise ValueError("Mes debe ser entre 1 y 12")
        utilidad_mensual = self.metas_ventas_mensuales[mes - 1] - self.gastos_fijos_mensuales[mes - 1]
        return utilidad_mensual


def main():
    if len(sys.argv) > 1:
        metas_ventas_mensuales = [float(x) for x in sys.argv[1:13]]
        gastos_fijos_mensuales = [float(x) for x in sys.argv[13:25]]
    else:
        metas_ventas_mensuales = [10000, 12000, 15000, 18000, 20000, 22000, 25000, 28000, 30000, 32000, 35000, 38000]
        gastos_fijos_mensuales = [5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500]
        print("Usando valores default:")
        print("Metas de ventas mensuales:", metas_ventas_mensuales)
        print("Gastos fijos mensuales:", gastos_fijos_mensuales)

    simulador = SimuladorUtilidades(metas_ventas_mensuales, gastos_fijos_mensuales)
    utilidades_anuales = simulador.calcular_utilidades_anuales()
    print("Utilidades anuales:", utilidades_anuales)

    mes = 6
    utilidad_mensual = simulador.calcular_utilidad_mensual(mes)
    print("Utilidad mensual para el mes", mes, ":", utilidad_mensual)


if __name__ == "__main__":
    main()