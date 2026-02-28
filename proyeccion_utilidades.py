"""
ÁREA: FINANZAS
DESCRIPCIÓN: Simulador de utilidades para calcular utilidades anuales y mensuales con consideraciones fiscales mexicanas
TECNOLOGÍA: Python
"""

import sys
import time
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

class SimuladorUtilidades:
    def __init__(self, metas_ventas_mensuales, gastos_fijos_mensuales):
        if len(metas_ventas_mensuales) != 12 or len(gastos_fijos_mensuales) != 12:
            raise ValueError("Se requieren exactamente 12 valores para metas de ventas y gastos fijos")
        self.metas_ventas_mensuales = metas_ventas_mensuales
        self.gastos_fijos_mensuales = gastos_fijos_mensuales
        self.tasa_impuesto = 0.30  # Tasa de impuestos aproximada en México

    def calcular_utilidades_anuales(self):
        utilidades_anuales = 0
        for i in range(12):
            utilidad_mensual = self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]
            utilidades_anuales += utilidad_mensual
        utilidad_neta = utilidades_anuales * (1 - self.tasa_impuesto)
        return utilidades_anuales, utilidad_neta

    def calcular_utilidad_mensual(self, mes):
        if mes < 1 or mes > 12:
            raise ValueError("Mes debe ser entre 1 y 12")
        utilidad_mensual = self.metas_ventas_mensuales[mes - 1] - self.gastos_fijos_mensuales[mes - 1]
        utilidad_neta = utilidad_mensual * (1 - self.tasa_impuesto)
        return utilidad_mensual, utilidad_neta

    def generar_resumen_ejecutivo(self):
        utilidades_brutas, utilidad_neta = self.calcular_utilidades_anuales()
        mes_mas_rentable = max(range(12), key=lambda i: self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]) + 1
        mes_menos_rentable = min(range(12), key=lambda i: self.metas_ventas_mensuales[i] - self.gastos_fijos_mensuales[i]) + 1

        return {
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "utilidad_bruta_anual": utilidades_brutas,
            "utilidad_neta_anual": utilidad_neta,
            "mes_mas_rentable": mes_mas_rentable,
            "mes_menos_rentable": mes_menos_rentable,
            "utilidad_promedio_mensual": utilidades_brutas / 12
        }

def main():
    if len(sys.argv) > 1:
        try:
            metas_ventas_mensuales = [float(x) for x in sys.argv[1:13]]
            gastos_fijos_mensuales = [float(x) for x in sys.argv[13:25]]
        except ValueError:
            print("Error: Todos los valores deben ser numéricos")
            return
    else:
        metas_ventas_mensuales = [10000, 12000, 15000, 18000, 20000, 22000, 25000, 28000, 30000, 32000, 35000, 38000]
        gastos_fijos_mensuales = [5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500]
        print("Usando valores default:")
        print("Metas de ventas mensuales:", metas_ventas_mensuales)
        print("Gastos fijos mensuales:", gastos_fijos_mensuales)