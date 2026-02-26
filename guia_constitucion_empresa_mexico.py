"""
AREA: LEGAL
DESCRIPCION: Agente que realiza guia constitucion empresa mexico
TECNOLOGIA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        nombre_empresa = sys.argv[1] if len(sys.argv) > 1 else "Empresa Mexicana SA de CV"
        fecha_constitucion = sys.argv[2] if len(sys.argv) > 2 else "2022-01-01"
        objeto_social = sys.argv[3] if len(sys.argv) > 3 else "Comercio al por mayor y al por menor"
        capital_social = float(sys.argv[4]) if len(sys.argv) > 4 else 100000.00
        numero_socios = int(sys.argv[5]) if len(sys.argv) > 5 else 2

        print(f"Nombre de la empresa: {nombre_empresa}")
        print(f"Fecha de constitución: {fecha_constitucion}")
        print(f"Objeto social: {objeto_social}")
        print(f"Capital social: ${capital_social:,.2f} MXN")
        print(f"Número de socios: {numero_socios}")
        print(f"Fecha de inicio de operaciones: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')}")
        print(f"Duración de la sociedad: 99 años a partir de la fecha de constitución")
        print(f"Tipo de sociedad: Sociedad Anónima de Capital Variable (SA de CV)")
        print(f"Domicilio fiscal: {sys.argv[6] if len(sys.argv) > 6 else 'Calle Ficticia 123, Ciudad de México, México'}")
        print(f"Registro Federal de Contribuyentes (RFC): {sys.argv[7] if len(sys.argv) > 7 else 'EMEXSA123456'}")
        print(f"Clave de identificación fiscal: {sys.argv[8] if len(sys.argv) > 8 else '1234567890123'}")
        print(f"Fecha de inicio de obligaciones fiscales: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=30)).strftime('%Y-%m-%d')}")
        print(f"Fecha de vencimiento de obligaciones fiscales: {(datetime.datetime.strptime(fecha_constitucion, '%Y-%m-%d') + datetime.timedelta(days=365)).strftime('%Y-%m-%d')}")
        print(f"Resumen ejecutivo: La empresa {nombre_empresa} se constituyó el {fecha_constitucion} con un capital social de ${capital_social:,.2f} MXN y {numero_socios} socios. La empresa iniciará operaciones 30 días después de la fecha de constitución y tendrá una duración de 99 años.")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()