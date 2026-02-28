"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza tracker pedidos basico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        clientes = ["Agencia Santi", "Distribuidora del Norte", "Supermercados del Sur"]
        productos = ["Refrescos", "Botanas", "Carnes", "Lácteos", "Frutas"]
        estados = ["En preparación", "En tránsito", "Entregado", "Retrasado", "Cancelado"]
        num_pedidos = int(sys.argv[1]) if len(sys.argv) > 1 else 10

        # Generar datos de ejemplo
        pedidos = []
        for i in range(1, num_pedidos + 1):
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
        print(f"Estados de pedidos: {', '.join(set(p['estado'] for p in pedidos))}")
        print(f"Fecha de entrega más temprana: {min(p['fecha_entrega'] for p in pedidos)}")
        print(f"Fecha de entrega más tardía: {max(p['fecha_entrega'] for p in pedidos)}")
        print("\nDetalle de pedidos:")
        for pedido in pedidos:
            print(f"  {pedido['id']}: {pedido['cliente']} - {pedido['producto']} ({pedido['cantidad']} unidades) - {pedido['estado']} - Entrega: {pedido['fecha_entrega']}")
        print("\nResumen ejecutivo:")
        print(f"Total de pedidos en preparación: {len([p for p in pedidos if p['estado'] == 'En preparación'])}")
        print(f"Total de pedidos en tránsito: {len([p for p in pedidos if p['estado'] == 'En tránsito'])}")
        print(f"Total de pedidos entregados: {len([p for p in pedidos if p['estado'] == 'Entregado'])}")
        print(f"Total de pedidos retrasados: {len([p for p in pedidos if p['estado'] == 'Retrasado'])}")
        print(f"Total de pedidos cancelados: {len([p for p in pedidos if p['estado'] == 'Cancelado'])}")

    except Exception as e:
        print(f"Error en el tracker: {str(e)}", file=sys.stderr)
    except IndexError:
        print("Error: Debe proporcionar el número de pedidos como argumento")

if __name__ == "__main__":
    main()