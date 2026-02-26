"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador ciclo venta
TECNOLOGÍA: Python estándar
"""
import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Parámetros por defecto
        dias_ciclo = 30
        ventas_diarias = 15
        conversion = 0.25
        ticket_promedio = 1250.50
        meta_mensual = 150000.00

        # Procesamiento
        ventas_mes = ventas_diarias * dias_ciclo
        ventas_convertidas = ventas_mes * conversion
        ingresos = ventas_convertidas * ticket_promedio
        porcentaje_meta = (ingresos / meta_mensual) * 100

        # Generar datos aleatorios para muestra
        datos_muestra = []
        for _ in range(5):
            fecha = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            clientes = random.randint(10, 25)
            ventas = random.randint(2, 5)
            datos_muestra.append({
                'fecha': fecha,
                'clientes': clientes,
                'ventas': ventas,
                'ingresos': round(ventas * ticket_promedio, 2)
            })

        # Salida
        print(f"Ciclo de ventas: {dias_ciclo} días")
        print(f"Ventas diarias promedio: {ventas_diarias} clientes")
        print(f"Tasa de conversión: {conversion*100:.1f}%")
        print(f"Ingresos proyectados: ${ingresos:,.2f} MXN")
        print(f"Cumplimiento de meta: {porcentaje_meta:.1f}%")
        print("\nDatos de muestra:")
        for dato in datos_muestra:
            print(f"{dato['fecha']}: {dato['clientes']} clientes, {dato['ventas']} ventas, ${dato['ingresos']:,.2f} MXN")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()