"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza analizador ciclo venta
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
        # Parámetros por defecto
        if len(sys.argv) > 1:
            dias_ciclo = int(sys.argv[1])
            ventas_diarias = int(sys.argv[2])
            conversion = float(sys.argv[3])
            ticket_promedio = float(sys.argv[4])
            meta_mensual = float(sys.argv[5])
        else:
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
        for _ in range(10):
            fecha = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            clientes = random.randint(10, 25)
            ventas = random.randint(2, 5)
            ingresos_muestra = round(ventas * ticket_promedio, 2)
            datos_muestra.append({
                'fecha': fecha,
                'clientes': clientes,
                'ventas': ventas,
                'ingresos': ingresos_muestra
            })

        # Salida
        print(f"Ciclo de ventas: {dias_ciclo} días")
        print(f"Ventas diarias promedio: {ventas_diarias} clientes")
        print(f"Tasa de conversión: {conversion*100:.1f}%")
        print(f"Ingresos proyectados: ${ingresos:,.2f} MXN")
        print(f"Cumplimiento de meta: {porcentaje_meta:.1f}%")
        print(f"Meta mensual: ${meta_mensual:,.2f} MXN")
        print(f"Ticket promedio: ${ticket_promedio:,.2f} MXN")
        print("\nDatos de muestra:")
        for i, dato in enumerate(datos_muestra):
            print(f"Dato {i+1}: {dato['fecha']}: {dato['clientes']} clientes, {dato['ventas']} ventas, ${dato['ingresos']:,.2f} MXN")
        print("\nResumen ejecutivo:")
        print(f"Se proyectan ingresos de ${ingresos:,.2f} MXN para el ciclo de ventas de {dias_ciclo} días.")
        print(f"La tasa de conversión es del {conversion*100:.1f}% y el ticket promedio es de ${ticket_promedio:,.2f} MXN.")
        print(f"El cumplimiento de la meta mensual es del {porcentaje_meta:.1f}%.")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")
    except ValueError:
        print("Error: Los parámetros deben ser numéricos.")
    except IndexError:
        print("Error: Faltan parámetros. Utilice el formato: python analizador_ciclo_venta.py dias_ciclo ventas_diarias conversion ticket_promedio meta_mensual")

if __name__ == "__main__":
    main()