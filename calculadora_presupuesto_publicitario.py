"""
ÁREA: MARKETING
DESCRIPCIÓN: Agente que realiza calculadora presupuesto publicitario
TECNOLOGÍA: Python estándar
"""

import sys
import math
import random

def calcula_presupuesto(inversión_total, porcentaje_publicidad):
    presupuesto_publicitario = inversión_total * (porcentaje_publicidad / 100)
    return presupuesto_publicitario

def calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter):
    costo_facebook = presupuesto_publicitario * (porcentaje_facebook / 100)
    costo_instagram = presupuesto_publicitario * (porcentaje_instagram / 100)
    costo_twitter = presupuesto_publicitario * (porcentaje_twitter / 100)
    return costo_facebook, costo_instagram, costo_twitter

def main():
    try:
        inversión_total = float(sys.argv[1]) if len(sys.argv) > 1 else 100000
        porcentaje_publicidad = float(sys.argv[2]) if len(sys.argv) > 2 else 20
        porcentaje_facebook = float(sys.argv[3]) if len(sys.argv) > 3 else 40
        porcentaje_instagram = float(sys.argv[4]) if len(sys.argv) > 4 else 30
        porcentaje_twitter = float(sys.argv[5]) if len(sys.argv) > 5 else 30

        presupuesto_publicitario = calcula_presupuesto(inversión_total, porcentaje_publicidad)
        costo_facebook, costo_instagram, costo_twitter = calcula_costo_por_plataforma(presupuesto_publicitario, porcentaje_facebook, porcentaje_instagram, porcentaje_twitter)

        print("Inversión total: $", inversión_total)
        print("Porcentaje de publicidad: ", porcentaje_publicidad, "%")
        print("Presupuesto publicitario: $", presupuesto_publicitario)
        print("Costo por plataforma:")
        print("  Facebook: $", costo_facebook)
        print("  Instagram: $", costo_instagram)
        print("  Twitter: $", costo_twitter)

    except Exception as e:
        print("Error: ", str(e))

if __name__ == "__main__":
    main()