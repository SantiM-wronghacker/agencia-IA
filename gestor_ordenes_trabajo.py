"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza gestor ordenes trabajo
TECNOLOGÍA: Python estándar
"""

import sys
import json
import os
from datetime import datetime, timedelta
import random
import math

def main():
    try:
        # Configuración por defecto
        fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        fecha_fin = datetime.now().strftime('%Y-%m-%d')
        limite_ordenes = 10
        iva = 0.16  # IVA para México

        # Procesar argumentos
        if len(sys.argv) > 1:
            fecha_inicio = sys.argv[1]
        if len(sys.argv) > 2:
            fecha_fin = sys.argv[2]
        if len(sys.argv) > 3:
            limite_ordenes = int(sys.argv[3])
        if len(sys.argv) > 4:
            iva = float(sys.argv[4])

        # Generar datos de órdenes de trabajo
        ordenes = []
        for i in range(1, limite_ordenes + 1):
            orden = {
                "id": f"OT-{random.randint(1000, 9999)}",
                "fecha": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
                "cliente": f"Cliente {random.randint(1, 100)}",
                "monto": round(random.uniform(500, 50000), 2),
                "monto_iva": round(random.uniform(500, 50000) * iva, 2),
                "monto_total": round(random.uniform(500, 50000) * (1 + iva), 2),
                "estatus": random.choice(["Pendiente", "En Proceso", "Completado", "Cancelado"]),
                "producto": f"Producto {random.randint(1, 20)}"
            }
            ordenes.append(orden)

        # Filtrar por fechas
        ordenes_filtradas = [o for o in ordenes if fecha_inicio <= o["fecha"] <= fecha_fin]

        # Mostrar resultados
        print("=== REPORTE DE ÓRDENES DE TRABAJO ===")
        print(f"Fecha de inicio: {fecha_inicio}")
        print(f"Fecha de fin: {fecha_fin}")
        print(f"Total de órdenes encontradas: {len(ordenes_filtradas)}")
        print("\nDetalles de las órdenes:")
        for orden in ordenes_filtradas:
            print(f"ID: {orden['id']}, Cliente: {orden['cliente']}, Monto: ${orden['monto']:.2f}, IVA: ${orden['monto_iva']:.2f}, Total: ${orden['monto_total']:.2f}, Estatus: {orden['estatus']}, Producto: {orden['producto']}")
        print("\nResumen de montos:")
        total_monto = sum([o["monto"] for o in ordenes_filtradas])
        total_iva = sum([o["monto_iva"] for o in ordenes_filtradas])
        total_total = sum([o["monto_total"] for o in ordenes_filtradas])
        print(f"Monto total: ${total_monto:.2f}")
        print(f"IVA total: ${total_iva:.2f}")
        print(f"Total general: ${total_total:.2f}")
        print("\nResumen ejecutivo:")
        print(f"Se encontraron {len(ordenes_filtradas)} órdenes de trabajo entre {fecha_inicio} y {fecha_fin}, con un total general de ${total_total:.2f}.")

    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}")

if __name__ == "__main__":
    main()