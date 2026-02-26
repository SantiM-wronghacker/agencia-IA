"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza plan migracion cloud
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
import datetime
import random

def main():
    try:
        # Parámetros por defecto
        args = sys.argv[1:]
        if len(args) > 0:
            cloud_provider = args[0]
        else:
            cloud_provider = "AWS"

        if len(args) > 1:
            budget_mxn = int(args[1])
        else:
            budget_mxn = 500000

        if len(args) > 2:
            deadline_days = int(args[2])
        else:
            deadline_days = 90

        # Generar datos de migración
        current_date = datetime.date.today()
        deadline_date = current_date + datetime.timedelta(days=deadline_days)

        # Cálculos ficticios pero realistas para México
        servers = random.randint(10, 30)
        storage_tb = round(random.uniform(50, 200), 2)
        cost_per_server = random.randint(5000, 15000)
        total_cost = servers * cost_per_server

        # Verificar presupuesto
        if total_cost > budget_mxn:
            budget_status = "SUPERADO"
            budget_diff = total_cost - budget_mxn
        else:
            budget_status = "DENTRO"
            budget_diff = budget_mxn - total_cost

        # Imprimir resultados
        print(f"Plan de Migración a {cloud_provider}")
        print(f"Fecha límite: {deadline_date.strftime('%d/%m/%Y')}")
        print(f"Servidores a migrar: {servers}")
        print(f"Almacenamiento total: {storage_tb} TB")
        print(f"Costo estimado: ${total_cost:,.2f} MXN ({budget_status} del presupuesto)")
        print(f"Diferencia presupuestal: ${abs(budget_diff):,.2f} MXN")

    except Exception as e:
        print(f"Error en la planificación: {str(e)}")

if __name__ == "__main__":
    main()