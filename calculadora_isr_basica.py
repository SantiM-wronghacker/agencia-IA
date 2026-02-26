"""
AREA: FINANZAS
DESCRIPCIÓN: Calculadora básica de ISR para empresarios.
TECNOLOGÍA: Python
"""

import sys
import math

class CalculadoraISRBasica:
    def __init__(self, ingresos_mensuales, deducciones, tarifa):
        self.ingresos_mensuales = ingresos_mensuales
        self.deducciones = deducciones
        self.tarifa = tarifa

    def calcular_isr(self):
        ingresos_netos = self.ingresos_mensuales - self.deducciones
        if ingresos_netos < 0:
            return 0
        isr = ingresos_netos * self.tarifa
        return isr

    def calcular_isr_porcentaje(self):
        isr = self.calcular_isr()
        if self.ingresos_mensuales == 0:
            return 0
        porcentaje = (isr / self.ingresos_mensuales) * 100
        return porcentaje

    def calcular_isr_anual(self):
        return self.calcular_isr() * 12

    def calcular_ingresos_netos_anuales(self):
        return (self.ingresos_mensuales - self.deducciones) * 12

def main():
    try:
        if len(sys.argv) == 4:
            ingresos_mensuales = float(sys.argv[1])
            deducciones = float(sys.argv[2])
            tarifa = float(sys.argv[3]) / 100
        else:
            ingresos_mensuales = 50000
            deducciones = 10000
            tarifa = 0.25
            print(f"Usando valores por defecto: ingresos_mensuales={ingresos_mensuales}, deducciones={deducciones}, tarifa={tarifa*100}%")

        if ingresos_mensuales < 0 or deducciones < 0 or tarifa < 0:
            raise ValueError("Valores no pueden ser negativos")

        calculadora = CalculadoraISRBasica(ingresos_mensuales, deducciones, tarifa)
        isr = calculadora.calcular_isr()
        porcentaje = calculadora.calcular_isr_porcentaje()
        isr_anual = calculadora.calcular_isr_anual()
        ingresos_netos_anuales = calculadora.calcular_ingresos_netos_anuales()

        print(f"ISR mensual: ${isr:.2f}")
        print(f"Porcentaje de ISR: {porcentaje:.2f}%")
        print(f"Ingresos mensuales: ${ingresos_mensuales:.2f}")
        print(f"Deducciones: ${deducciones:.2f}")
        print(f"Tarifa del ISR: {tarifa*100}%")
        print(f"ISR anual: ${isr_anual:.2f}")
        print(f"Ingresos netos anuales: ${ingresos_netos_anuales:.2f}")
        print(f"Resumen ejecutivo: El ISR mensual es de ${isr:.2f} y el porcentaje de ISR es de {porcentaje:.2f}%. El ISR anual es de ${isr_anual:.2f} y los ingresos netos anuales son de ${ingresos_netos_anuales:.2f}.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()