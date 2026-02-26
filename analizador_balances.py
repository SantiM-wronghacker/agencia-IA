"""
ÁREA: FINANZAS
DESCRIPCIÓN: Analiza un archivo de texto con activos y pasivos para calcular el capital contable y razones financieras básicas.
TECNOLOGÍA: Python
"""

import os
import sys
import time

class AnalizadorBalances:
    def __init__(self, archivo):
        self.archivo = archivo
        self.activos = {}
        self.pasivos = {}
        self.capital_contable = 0

    def leer_archivo(self):
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for linea in f:
                    linea = linea.strip()
                    if not linea:
                        continue
                    elementos = linea.split(',')
                    if elementos[0] == 'Activo':
                        self.activos[elementos[1]] = float(elementos[2])
                    elif elementos[0] == 'Pasivo':
                        self.pasivos[elementos[1]] = float(elementos[2])
        except FileNotFoundError:
            print("El archivo no existe")
            return None

    def calcular_capital_contable(self):
        total_activos = sum(self.activos.values())
        total_pasivos = sum(self.pasivos.values())
        self.capital_contable = total_activos - total_pasivos

    def calcular_razones_financieras(self):
        if self.capital_contable == 0:
            return None
        liquidez = self.activos.get('Caja y bancos', 0) / self.pasivos.get('Cuentas por pagar', 1)
        endeudamiento = sum(self.pasivos.values()) / self.capital_contable
        return liquidez, endeudamiento

    def imprimir_resultados(self):
        print("Capital Contable:", self.capital_contable)
        razones = self.calcular_razones_financieras()
        if razones:
            print("Liquidez:", razones[0])
            print("Endeudamiento:", razones[1])

def main():
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        archivo = 'balances.txt'
        print("Usando archivo por defecto:", archivo)
    analizador = AnalizadorBalances(archivo)
    analizador.leer_archivo()
    analizador.calcular_capital_contable()
    analizador.imprimir_resultados()

if __name__ == "__main__":
    main()