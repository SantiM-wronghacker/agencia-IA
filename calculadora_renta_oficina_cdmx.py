"""
ÁREA: BIENES RAÍCES COMERCIALES
DESCRIPCIÓN: Agente que realiza calculadora renta oficina cdmx
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_renta_oficina():
    # Parámetros por defecto realistas para CDMX
    metros_cuadrados = float(sys.argv[1]) if len(sys.argv) > 1 else 50.0
    zona = sys.argv[2] if len(sys.argv) > 2 else "Reforma"
    mantenimiento = float(sys.argv[3]) if len(sys.argv) > 3 else 0.15
    estacionamiento = sys.argv[4] if len(sys.argv) > 4 else "no"

    # Tarifas por zona (pesos por m2/mes)
    tarifas = {
        "Polanco": 1200,
        "Reforma": 950,
        "Santa Fe": 1050,
        "Condesa": 1100,
        "Roma": 900
    }

    # Cálculo base
    renta_base = metros_cuadrados * tarifas.get(zona, 800)  # 800 default si no está en el diccionario

    # Cálculo de mantenimiento
    mantenimiento_mensual = renta_base * mantenimiento

    # Costo estacionamiento (si aplica)
    estacionamiento_costo = 0
    if estacionamiento.lower() == "si":
        estacionamiento_costo = 3500

    # Cálculo total
    total_mensual = renta_base + mantenimiento_mensual + estacionamiento_costo
    anual = total_mensual * 12

    return {
        "metros_cuadrados": metros_cuadrados,
        "zona": zona,
        "renta_base_mensual": round(renta_base, 2),
        "mantenimiento_mensual": round(mantenimiento_mensual, 2),
        "estacionamiento": estacionamiento,
        "total_mensual": round(total_mensual, 2),
        "total_anual": round(anual, 2)
    }

def main():
    try:
        resultados = calcular_renta_oficina()

        print("Cálculo de renta para oficina en CDMX:")
        print(f"1. Área: {resultados['metros_cuadrados']} m² en zona {resultados['zona']}")
        print(f"2. Renta base mensual: ${resultados['renta_base_mensual']:,}")
        print(f"3. Mantenimiento mensual: ${resultados['mantenimiento_mensual']:,}")
        print(f"4. Incluye estacionamiento: {resultados['estacionamiento']} (${estacionamiento_costo:,} si aplica)")
        print(f"5. Total mensual: ${resultados['total_mensual']:,}")
        print(f"6. Total anual: ${resultados['total_anual']:,}")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_renta_oficina_cdmx.py [metros] [zona] [mantenimiento] [estacionamiento]")
        print("Ejemplo: calculadora_renta_oficina_cdmx.py 60 Polanco 0.15 si")

if __name__ == "__main__":
    main()