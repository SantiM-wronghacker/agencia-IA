"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza calculadora presupuesto publicitario
TECNOLOGÍA: Python estándar
"""

import sys
import math
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_presupuesto(inversión_total, porcentaje_publicidad):
    presupuesto_publicitario = inversión_total * (porcentaje_publicidad / 100)
    return presupuesto_publicitario

def calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter):
    costo_facebook = presupuesto_publicitario * (porcentaje_facebook / 100)
    costo_instagram = presupuesto_publicitario * (porcentaje_instagram / 100)
    costo_twitter = presupuesto_publicitario * (porcentaje_twitter / 100)
    return costo_facebook, costo_instagram, costo_twitter

def calcula_impuesto(presupuesto_publicitario):
    impuesto = presupuesto_publicitario * 0.16
    return impuesto

def calcula_total_con_impuesto(presupuesto_publicitario, impuesto):
    total_con_impuesto = presupuesto_publicitario + impuesto
    return total_con_impuesto

def main():
    try:
        inversión_total = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
        porcentaje_publicidad = float(sys.argv[2]) if len(sys.argv) > 2 else 20
        porcentaje_facebook = float(sys.argv[3]) if len(sys.argv) > 3 else 40
        porcentaje_instagram = float(sys.argv[4]) if len(sys.argv) > 4 else 30
        porcentaje_twitter = float(sys.argv[5]) if len(sys.argv) > 5 else 30

        presupuesto_publicitario = calcula_presupuesto(inversión_total, porcentaje_publicidad)
        costo_facebook, costo_instagram, costo_twitter = calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter)
        impuesto = calcula_impuesto(presupuesto_publicitario)
        total_con_impuesto = calcula_total_con_impuesto(presupuesto_publicitario, impuesto)

        print("Inversión total: $", inversión_total)
        print("Porcentaje de publicidad: ", porcentaje_publicidad, "%")
        print("Presupuesto publicitario: $", presupuesto_publicitario)
        print("Costo por plataforma:")
        print("  Facebook: $", costo_facebook)
        print("  Instagram: $", costo_instagram)
        print("  Twitter: $", costo_twitter)
        print("Impuesto (16%): $", impuesto)
        print("Total con impuesto: $", total_con_impuesto)
        print("Resumen ejecutivo:")
        print("  Se ha calculado un presupuesto publicitario de $", presupuesto_publicitario, "con un impuesto de $", impuesto, "y un total con impuesto de $", total_con_impuesto)
        print("  La distribución del presupuesto es: Facebook ($", costo_facebook, "), Instagram ($", costo_instagram, ") y Twitter ($", costo_twitter, ")")

    except ValueError:
        print("Error: Los valores ingresados deben ser numéricos")
    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()