"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora costo envio mexico con tarifas realistas
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_costo_envio(origen, destino, peso, distancia):
    # Tarifas realistas para México (2023)
    COSTO_FIJO = 50.00
    COSTO_KM = 15.50
    COSTO_KG = 22.75
    COSTO_MINIMO = 100.00

    # Ajuste por zona (ejemplo: 10% más caro a zonas remotas)
    zonas_remotas = ['Chihuahua', 'Durango', 'Baja California Sur']
    factor_zona = 1.10 if destino in zonas_remotas else 1.00

    # Validaciones
    if peso <= 0:
        raise ValueError("El peso debe ser mayor a 0 kg")
    if distancia <= 0:
        raise ValueError("La distancia debe ser mayor a 0 km")

    # Cálculo del costo total
    costo_distancia = distancia * COSTO_KM * factor_zona
    costo_peso = peso * COSTO_KG
    costo_total = max(COSTO_FIJO + costo_distancia + costo_peso, COSTO_MINIMO)

    return {
        "origen": origen,
        "destino": destino,
        "peso_kg": peso,
        "distancia_km": distancia,
        "costo_distancia": round(costo_distancia, 2),
        "costo_peso": round(costo_peso, 2),
        "costo_fijo": COSTO_FIJO,
        "costo_total": round(costo_total, 2),
        "factor_zona": factor_zona,
        "es_zona_remota": destino in zonas_remotas
    }

def main():
    try:
        # Parámetros por defecto realistas
        origen = sys.argv[1] if len(sys.argv) > 1 else "CDMX"
        destino = sys.argv[2] if len(sys.argv) > 2 else "Guadalajara"
        peso = float(sys.argv[3]) if len(sys.argv) > 3 else 5.2
        distancia = float(sys.argv[4]) if len(sys.argv) > 4 else 550.0

        resultado = calcular_costo_envio(origen, destino, peso, distancia)

        print("=== DETALLES DEL ENVÍO ===")
        print(f"Ruta: {resultado['origen']} → {resultado['destino']}")
        print(f"Peso: {resultado['peso_kg']} kg | Distancia: {resultado['distancia_km']} km")
        print(f"Zona remota: {'Sí' if resultado['es_zona_remota'] else 'No'} (Factor {resultado['factor_zona']})")
        print("=== DESGLOSE DE COSTOS ===")
        print(f"Costo fijo: ${resultado['costo_fijo']}")
        print(f"Costo por distancia: ${resultado['costo_distancia']}")
        print(f"Costo por peso: ${resultado['costo_peso']}")
        print("=== RESUMEN ===")
        print(f"Costo total estimado: ${resultado['costo_total']}")
        print("=== RECOMENDACIONES ===")
        print("Considerar seguro para envíos >$500 o paquetes frágiles")
        print("Verificar restricciones de peso para destino")

    except ValueError as ve:
        print(f"Error de validación: {str(ve)}")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
    finally:
        print("\nUso: calculadora_costo_envio_mexico.py <origen> <destino> <peso_kg> <distancia_km>")
        print("Ejemplo: calculadora_costo_envio_mexico.py CDMX Monterrey 3.5 1200")

if __name__ == "__main__":
    main()