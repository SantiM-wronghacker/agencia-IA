"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza calculadora costo infraestructura cloud
TECNOLOGÍA: Python estándar
"""
import sys
import json
import math
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        region = sys.argv[1] if len(sys.argv) > 1 else "mexico"
        tipo_instancia = sys.argv[2] if len(sys.argv) > 2 else "t2.micro"
        horas_mes = int(sys.argv[3]) if len(sys.argv) > 3 else 730
        tipo_pago = sys.argv[4] if len(sys.argv) > 4 else "on-demand"

        # Precios en MXN (ejemplo con AWS)
        precios = {
            "mexico": {
                "t2.micro": {"on-demand": 0.022, "reserved": 0.015},
                "t2.small": {"on-demand": 0.044, "reserved": 0.030},
                "t2.medium": {"on-demand": 0.088, "reserved": 0.060}
            },
            "us-east": {
                "t2.micro": {"on-demand": 0.019, "reserved": 0.013},
                "t2.small": {"on-demand": 0.038, "reserved": 0.026},
                "t2.medium": {"on-demand": 0.076, "reserved": 0.052}
            }
        }

        # Cálculo
        costo_hora = precios[region].get(tipo_instancia, {}).get(tipo_pago, 0.022)
        costo_mes = costo_hora * horas_mes
        costo_anual = costo_mes * 12
        impuesto = costo_anual * 0.16  # 16% de impuesto
        costo_total = costo_anual + impuesto

        # Output
        print(f"Región: {region}")
        print(f"Tipo de instancia: {tipo_instancia}")
        print(f"Tipo de pago: {tipo_pago}")
        print(f"Costo por hora: ${costo_hora:.2f} MXN")
        print(f"Costo mensual (730h): ${costo_mes:.2f} MXN")
        print(f"Costo anual: ${costo_anual:.2f} MXN")
        print(f"Impuesto anual (16%): ${impuesto:.2f} MXN")
        print(f"Costo total anual: ${costo_total:.2f} MXN")
        print(f"Fecha de cálculo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Horas de uso al mes: {horas_mes} horas")
        print(f"Resumen ejecutivo: El costo total anual para la región {region} con tipo de instancia {tipo_instancia} y tipo de pago {tipo_pago} es de ${costo_total:.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: python calculadora_costo_infraestructura_cloud.py [region] [tipo_instancia] [horas_mes] [tipo_pago]")
        print("Ejemplo: python calculadora_costo_infraestructura_cloud.py mexico t2.micro 730 on-demand")

if __name__ == "__main__":
    main()