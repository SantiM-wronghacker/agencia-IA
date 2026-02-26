"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que realiza generador descripcion puesto
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        nombre_puesto = sys.argv[1] if len(sys.argv) > 1 else "Gerente de Ventas"
        sueldo_anual = int(sys.argv[2]) if len(sys.argv) > 2 else 500000
        beneficios = ["Seguro médico", "Bono de vacaciones", "Plan de pensiones", "Aguinaldo", "Prima de antigüedad"]
        beneficios_random = random.sample(beneficios, 3)
        fecha_inicio = datetime.date.today()
        fecha_fin = datetime.date.today() + datetime.timedelta(days=365)

        print(f"Nombre del puesto: {nombre_puesto}")
        print(f"Sueldo anual: ${sueldo_anual:,.2f} MXN")
        print(f"Sueldo mensual: ${sueldo_anual / 12:,.2f} MXN")
        print(f"Beneficios: {', '.join(beneficios_random)}")
        print(f"Fecha de inicio: {fecha_inicio.strftime('%d/%m/%Y')}")
        print(f"Fecha de fin: {fecha_fin.strftime('%d/%m/%Y')}")
        print(f"Duración del contrato: {math.ceil((fecha_fin - fecha_inicio).days / 365)} años")
        print(f"IMPUESTO SOBRE LA RENTA (ISR): {sueldo_anual * 0.1:,.2f} MXN")
        print(f"SUBSIDIO PARA EL EMPLEO: {sueldo_anual * 0.01:,.2f} MXN")
        print(f"APORTACIONES AL IMSS: {sueldo_anual * 0.05:,.2f} MXN")
        print(f"APORTACIONES AL INFONAVIT: {sueldo_anual * 0.05:,.2f} MXN")

        print("\nResumen Ejecutivo:")
        print(f"El puesto de {nombre_puesto} ofrece un sueldo anual de ${sueldo_anual:,.2f} MXN, beneficios como {', '.join(beneficios_random)} y una duración del contrato de {math.ceil((fecha_fin - fecha_inicio).days / 365)} años.")

    except ValueError as e:
        print(f"Error: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()