"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente que realiza calculadora renta justa m2
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_renta_justa(m2, ubicacion, tipo_inmueble):
    """
    Calcula la renta justa por m2 según la ubicación y tipo de inmueble
    """
    precios_por_m2 = {
        'centro': 800,
        'norte': 600,
        'sur': 500,
    }

    ajustes_por_tipo = {
        'departamento': 1.2,
        'casa': 0.8,
    }

    precio_base = precios_por_m2.get(ubicacion, 500)
    ajuste_por_tipo = ajustes_por_tipo.get(tipo_inmueble, 1.0)

    renta_justa = precio_base * ajuste_por_tipo * m2

    return renta_justa

def calcula_impuestos(renta_justa):
    """
    Calcula los impuestos sobre la renta justa
    """
    impuesto_isr = renta_justa * 0.08
    impuesto_iva = renta_justa * 0.16
    return impuesto_isr, impuesto_iva

def main():
    try:
        m2 = int(sys.argv[1]) if len(sys.argv) > 1 else 100
        ubicacion = sys.argv[2] if len(sys.argv) > 2 else 'centro'
        tipo_inmueble = sys.argv[3] if len(sys.argv) > 3 else 'departamento'

        renta_justa = calcula_renta_justa(m2, ubicacion, tipo_inmueble)
        impuesto_isr, impuesto_iva = calcula_impuestos(renta_justa)

        print(f"Renta justa por {m2} m2 en {ubicacion} para {tipo_inmueble}: ${renta_justa:.2f} MXN")
        print(f"Renta justa por m2 en {ubicacion} para {tipo_inmueble}: ${renta_justa / m2:.2f} MXN/m2")
        print(f"Ajuste por tipo de inmueble: {tipo_inmueble} ({1.2 if tipo_inmueble == 'departamento' else 0.8})")
        print(f"Precio base por m2 en {ubicacion}: ${800 if ubicacion == 'centro' else 600 if ubicacion == 'norte' else 500} MXN/m2")
        print(f"Ubicación: {ubicacion}, Tipo de inmueble: {tipo_inmueble}")
        print(f"Impuesto ISR: ${impuesto_isr:.2f} MXN")
        print(f"Impuesto IVA: ${impuesto_iva:.2f} MXN")
        print(f"Total de impuestos: ${impuesto_isr + impuesto_iva:.2f} MXN")
        print(f"Renta neta: ${renta_justa - impuesto_isr - impuesto_iva:.2f} MXN")

        print("\nResumen Ejecutivo:")
        print(f"Renta justa: ${renta_justa:.2f} MXN")
        print(f"Impuestos: ${impuesto_isr + impuesto_iva:.2f} MXN")
        print(f"Renta neta: ${renta_justa - impuesto_isr - impuesto_iva:.2f} MXN")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()