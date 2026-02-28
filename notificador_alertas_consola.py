"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza notificador alertas consola
TECNOLOGÍA: Python estándar
"""
import sys
import json
import os
from datetime import datetime
import random
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_porcentaje(parcial, total):
    if total == 0:
        return 0
    return round((parcial / total) * 100, 2)

def calcular_iva(monto):
    return round(monto * 0.16, 2)

def main():
    try:
        # Configuración por defecto
        alertas = [
            {"id": 1, "tipo": "VENTAS", "mensaje": "Ventas diarias: $15,250.00 MXN", "prioridad": "ALTA"},
            {"id": 2, "tipo": "INVENTARIO", "mensaje": "Stock crítico: 35 unidades de producto XYZ", "prioridad": "MEDIA"},
            {"id": 3, "tipo": "FINANZAS", "mensaje": "Gasto mensual: $48,750.00 MXN", "prioridad": "BAJA"},
            {"id": 4, "tipo": "LOGISTICA", "mensaje": "Envíos pendientes: 12", "prioridad": "ALTA"},
            {"id": 5, "tipo": "SOPORTE", "mensaje": "Tickets abiertos: 7", "prioridad": "MEDIA"}
        ]

        # Procesar argumentos
        if len(sys.argv) > 1:
            try:
                archivo = sys.argv[1]
                if os.path.exists(archivo):
                    with open(archivo, 'r') as f:
                        alertas = json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error al leer el archivo: {e}")
                sys.exit(1)

        # Datos adicionales calculados
        total_ventas = 15250.00
        total_gastos = 48750.00
        iva = calcular_iva(total_ventas)
        margen = total_ventas - total_gastos
        porcentaje_margen = calcular_porcentaje(margen, total_ventas)

        # Mostrar alertas
        print("=== NOTIFICADOR DE ALERTAS ===")
        print(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Total de alertas: {len(alertas)}")
        print("Alertas activas:")
        for alerta in alertas:
            print(f"  {alerta['id']}. {alerta['tipo']} ({alerta['prioridad']}): {alerta['mensaje']}")

        # Datos financieros
        print("\n=== RESUMEN FINANCIERO ===")
        print(f"Ventas diarias: ${total_ventas:,.2f} MXN")
        print(f"Gastos mensuales: ${total_gastos:,.2f} MXN")
        print(f"IVA (16%): ${iva:,.2f} MXN")
        print(f"Margen bruto: ${margen:,.2f} MXN ({porcentaje_margen}%)")

        # Resumen ejecutivo
        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Operación: {'Positiva' if margen > 0 else 'Negativa'}")
        print(f"Prioridad crítica: {sum(1 for a in alertas if a['prioridad'] == 'ALTA')}")
        print(f"Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

    except Exception as e:
        print(f"Error en el notificador: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()