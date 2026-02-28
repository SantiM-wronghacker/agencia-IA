"""
ÁREA: VENTAS
DESCRIPCIÓN: Agente que realiza generador argumentario ventas
TECNOLOGÍA: Python estándar
"""

import sys
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        producto = sys.argv[1] if len(sys.argv) > 1 else "Seguro de Auto"
        cliente = sys.argv[2] if len(sys.argv) > 2 else "Cliente Premium"
        meses = int(sys.argv[3]) if len(sys.argv) > 3 else 12
        descuento = float(sys.argv[4]) if len(sys.argv) > 4 else 15.5
        coberturas = sys.argv[5] if len(sys.argv) > 5 else "Básica, Ampliada, Total"

        # Generación de argumentario
        print(f"Argumentario para {producto} - {cliente}")
        print(f"1. Oferta especial: {descuento}% de descuento en {meses} meses")
        print(f"2. Coberturas disponibles: {coberturas}")
        precio_mensual = random.randint(500, 2000)
        print(f"3. Precio mensual estimado: ${precio_mensual:,.2f} MXN")
        print(f"4. Beneficio adicional: {random.choice(['Asistencia vial 24/7', 'Protección legal', 'Reembolso de gastos médicos'])}")
        fecha_inicial = datetime.now().strftime('%d/%m/%Y')
        fecha_final = datetime.now().replace(year=datetime.now().year + 1).strftime('%d/%m/%Y')
        print(f"5. Fecha de vigencia: {fecha_inicial} a {fecha_final}")
        print(f"6. Precio total estimado: ${precio_mensual * meses:,.2f} MXN")
        print(f"7. Ahorro estimado con descuento: ${precio_mensual * meses * (descuento / 100):,.2f} MXN")
        print(f"8. Precio total con descuento: ${precio_mensual * meses * (1 - descuento / 100):,.2f} MXN")
        print(f"9. Impuestos aplicables (16% IVA): ${precio_mensual * meses * (1 - descuento / 100) * 0.16:,.2f} MXN")
        print(f"10. Precio total con impuestos: ${precio_mensual * meses * (1 - descuento / 100) * 1.16:,.2f} MXN")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"Producto: {producto}")
        print(f"Cliente: {cliente}")
        print(f"Plazo: {meses} meses")
        print(f"Descuento: {descuento}%")
        print(f"Precio total con descuento e impuestos: ${precio_mensual * meses * (1 - descuento / 100) * 1.16:,.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: generador_argumentario_ventas.py [producto] [cliente] [meses] [descuento] [coberturas]")

if __name__ == "__main__":
    main()