"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza checklist contratacion seguro
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

def calcular_prima(edad, sexo, estado_civil):
    prima = 0
    if edad < 20:
        prima += 800
    elif edad < 25:
        prima += 600
    elif edad < 35:
        prima += 750
    elif edad < 45:
        prima += 1000
    elif edad < 55:
        prima += 1200
    else:
        prima += 1500

    if sexo == "M":
        prima += 250
    elif sexo == "F":
        prima += 200

    if estado_civil == "Casado":
        prima -= 100
    elif estado_civil == "Soltero":
        prima += 50
    elif estado_civil == "Divorciado":
        prima += 100
    elif estado_civil == "Viudo":
        prima += 150

    return prima

def calcular_deducible(monto_asegurado):
    deducible = monto_asegurado * 0.1
    return deducible

def calcular_comision(prima):
    comision = prima * 0.05
    return comision

def calcular_iva(prima):
    iva = prima * 0.16
    return iva

def main():
    try:
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        sexo = sys.argv[2] if len(sys.argv) > 2 else "M"
        estado_civil = sys.argv[3] if len(sys.argv) > 3 else "Soltero"
        monto_asegurado = int(sys.argv[4]) if len(sys.argv) > 4 else 100000

        prima = calcular_prima(edad, sexo, estado_civil)
        deducible = calcular_deducible(monto_asegurado)
        comision = calcular_comision(prima)
        iva = calcular_iva(prima)

        print("Edad:", edad)
        print("Sexo:", sexo)
        print("Estado civil:", estado_civil)
        print("Monto asegurado: $", monto_asegurado)
        print("Prima anual: $", prima)
        print("Deducible: $", deducible)
        print("Comisión: $", comision)
        print("IVA: $", iva)
        print("Total a pagar: $", prima + comision + iva)
        print("Fecha de inicio de vigencia:", datetime.date.today().strftime("%Y-%m-%d"))
        print("Fecha de fin de vigencia:", (datetime.date.today() + datetime.timedelta(days=365)).strftime("%Y-%m-%d"))
        print("Resumen ejecutivo:")
        print("El cliente de", edad, "años, sexo", sexo, "y estado civil", estado_civil, "debe pagar una prima anual de $", prima)
        print("Además, debe pagar un deducible de $", deducible, "y una comisión de $", comision)
        print("El total a pagar es de $", prima + comision + iva)
    except Exception as e:
        print("Error:", str(e))
    except ValueError:
        print("Error: Los valores ingresados no son válidos")
    except IndexError:
        print("Error: No se han ingresado todos los valores necesarios")

if __name__ == "__main__":
    main()