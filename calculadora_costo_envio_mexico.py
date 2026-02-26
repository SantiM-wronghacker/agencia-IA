"""
ÁREA: LOGÍSTICA
DESCRIPCIÓN: Agente que realiza calculadora costo envio mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcular_costo_envio(origen, destino, peso, distancia):
    # Costos base por kilómetro (MXN)
    costo_km = 15.50
    # Costo por kilogramo (MXN)
    costo_kg = 22.75
    # Costo fijo por envío (MXN)
    costo_fijo = 50.00

    # Cálculo del costo total
    costo_distancia = distancia * costo_km
    costo_peso = peso * costo_kg
    costo_total = costo_fijo + costo_distancia + costo_peso

    return {
        "origen": origen,
        "destino": destino,
        "peso_kg": peso,
        "distancia_km": distancia,
        "costo_distancia": round(costo_distancia, 2),
        "costo_peso": round(costo_peso, 2),
        "costo_fijo": costo_fijo,
        "costo_total": round(costo_total, 2)
    }

def main():
    try:
        # Parámetros por defecto realistas
        origen = sys.argv[1] if len(sys.argv) > 1 else "CDMX"
        destino = sys.argv[2] if len(sys.argv) > 2 else "Guadalajara"
        peso = float(sys.argv[3]) if len(sys.argv) > 3 else 5.2
        distancia = float(sys.argv[4]) if len(sys.argv) > 4 else 550.0

        resultado = calcular_costo_envio(origen, destino, peso, distancia)

        print(f"Ruta: {resultado['origen']} a {resultado['destino']}")
        print(f"Peso: {resultado['peso_kg']} kg")
        print(f"Distancia: {resultado['distancia_km']} km")
        print(f"Costo por distancia: ${resultado['costo_distancia']}")
        print(f"Costo por peso: ${resultado['costo_peso']}")
        print(f"Costo total: ${resultado['costo_total']}")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: calculadora_costo_envio_mexico.py <origen> <destino> <peso_kg> <distancia_km>")
        print("Ejemplo: calculadora_costo_envio_mexico.py CDMX Monterrey 3.5 1200")

if __name__ == "__main__":
    main()