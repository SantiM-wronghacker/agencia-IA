"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza generador acta acuerdos
TECNOLOGÍA: Python estándar
"""

import sys
import json
from datetime import datetime, timedelta
import random

def generar_acta_acuerdos(participantes=None, temas=None, numero_acta=None):
    if participantes is None:
        participantes = ["Juan Pérez", "María García", "Carlos López", "Ana Martínez"]
    if temas is None:
        temas = ["Revisión de contratos", "Presupuesto anual", "Nuevos proyectos"]
    if numero_acta is None:
        numero_acta = random.randint(1000, 9999)

    # Datos base
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    hora_actual = datetime.now().strftime("%H:%M")
    fecha_proxima_reunion = (datetime.now() + timedelta(days=7)).strftime("%d/%m/%Y")

    # Generar acta
    acta = f"""
ACTA DE ACUERDOS
Número: {numero_acta}
Fecha: {fecha_actual}
Hora: {hora_actual}

Asistentes:
"""
    for participante in participantes:
        acta += f"- {participante}\n"

    acta += """
Temas tratados:
"""
    for i, tema in enumerate(temas, start=1):
        acta += f"{i}. {tema}\n"

    acta += """
Acuerdos tomados:
1. Aprobación del presupuesto anual con un monto de $1,200,000.00 MXN
2. Asignación de $350,000.00 MXN para nuevos proyectos
3. Revisión de contratos con fecha límite 15/12/2023

Responsables:
"""
    for i, participante in enumerate(participantes):
        acta += f"- {participante}: {temas[i % len(temas)]}\n"

    acta += f"""
Próxima reunión: {fecha_proxima_reunion}

Resumen Ejecutivo:
Se aprobó el presupuesto anual y se asignaron fondos para nuevos proyectos. Se estableció una fecha límite para la revisión de contratos.
"""
    return acta

def main():
    try:
        if len(sys.argv) > 1:
            participantes = sys.argv[1].split(",")
            temas = sys.argv[2].split(",")
            numero_acta = int(sys.argv[3])
        else:
            participantes = None
            temas = None
            numero_acta = None

        acta = generar_acta_acuerdos(participantes, temas, numero_acta)
        print(acta)
    except Exception as e:
        print(f"Error al generar el acta: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()