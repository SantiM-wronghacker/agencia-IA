"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza calculo nomina mensual mexico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calculo_nomina(salario_diario, dias_trabajados):
    try:
        salario_mensual = salario_diario * dias_trabajados
        impuesto = salario_mensual * 0.16  # 16% de impuesto sobre la renta
        seguro_social = salario_mensual * 0.11  # 11% de seguro social
        infonavit = salario_mensual * 0.05  # 5% de infonavit
        total_deducciones = impuesto + seguro_social + infonavit
        neto = salario_mensual - total_deducciones
        return {
            "salario_mensual": salario_mensual,
            "impuesto": impuesto,
            "seguro_social": seguro_social,
            "infonavit": infonavit,
            "total_deducciones": total_deducciones,
            "neto": neto
        }
    except Exception as e:
        return str(e)

def main():
    try:
        if len(sys.argv) < 3:
            print("Uso: python calculo_nomina_mensual_mexico.py <salario_diario> <dias_trabajados>")
            print("Ejemplo: python calculo_nomina_mensual_mexico.py 500.0 30")
            return
        salario_diario = float(sys.argv[1])
        dias_trabajados = int(sys.argv[2])
        resultado = calculo_nomina(salario_diario, dias_trabajados)
        if isinstance(resultado, dict):
            print("Resumen de Nómina:")
            print("--------------------")
            print("Salario Diario: $", round(salario_diario, 2))
            print("Días Trabajados: ", dias_trabajados)
            print("Salario Mensual: $", round(resultado["salario_mensual"], 2))
            print("Impuesto (16%): $", round(resultado["impuesto"], 2))
            print("Seguro Social (11%): $", round(resultado["seguro_social"], 2))
            print("Infonavit (5%): $", round(resultado["infonavit"], 2))
            print("Total Deducciones: $", round(resultado["total_deducciones"], 2))
            print("Neto: $", round(resultado["neto"], 2))
            print("\nResumen Ejecutivo:")
            print("--------------------")
            print("El salario mensual es de $", round(resultado["salario_mensual"], 2))
            print("Las deducciones totales son de $", round(resultado["total_deducciones"], 2))
            print("El monto neto a recibir es de $", round(resultado["neto"], 2))
        else:
            print("Error:", resultado)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    main()