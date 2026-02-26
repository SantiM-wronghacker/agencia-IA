"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza tracker pedidos basico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Configuración por defecto
        clientes = ["Agencia Santi", "Distribuidora del Norte", "Supermercados del Sur"]
        productos = ["Refrescos", "Botanas", "Carnes", "Lácteos", "Frutas"]
        estados = ["En preparación", "En tránsito", "Entregado", "Retrasado", "Cancelado"]

        # Generar datos de ejemplo
        pedidos = []
        for i in range(1, 6):
            cliente = random.choice(clientes)
            producto = random.choice(productos)
            cantidad = random.randint(10, 100)
            fecha_entrega = datetime.now() + timedelta(days=random.randint(1, 7))
            estado = random.choice(estados)
            pedidos.append({
                "id": f"PED-{i:04d}",
                "cliente": cliente,
                "producto": producto,
                "cantidad": cantidad,
                "fecha_entrega": fecha_entrega.strftime("%Y-%m-%d"),
                "estado": estado
            })

        # Mostrar resultados
        print("=== TRACKER DE PEDIDOS BÁSICO ===")
        print(f"Fecha de reporte: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total de pedidos: {len(pedidos)}")
        print(f"Productos más comunes: {', '.join(set(p['producto'] for p in pedidos))}")
        print(f"Clientes atendidos: {', '.join(set(p['cliente'] for p in pedidos))}")
        print("\nDetalle de pedidos:")
        for pedido in pedidos:
            print(f"  {pedido['id']}: {pedido['cliente']} - {pedido['producto']} ({pedido['cantidad']} unidades) - {pedido['estado']}")

    except Exception as e:
        print(f"Error en el tracker: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    main()