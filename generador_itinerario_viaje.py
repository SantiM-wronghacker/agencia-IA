"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador itinerario viaje
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Parámetros por defecto
        destino = sys.argv[1] if len(sys.argv) > 1 else "Cancún"
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 7
        presupuesto = float(sys.argv[3]) if len(sys.argv) > 3 else 15000.0

        # Datos de ejemplo para destinos en México
        destinos = {
            "Cancún": {"hoteles": ["Riu Palace", "Hyatt Ziva", "Grand Fiesta Americana"],
                      "actividades": ["Playa Delfines", "Xcaret", "Isla Mujeres"],
                      "gastos_diarios": 1200.0},
            "CDMX": {"hoteles": ["W Mexico City", "Four Seasons", "Grand Fiesta Americana"],
                     "actividades": ["Zócalo", "Teotihuacán", "Museo Frida Kahlo"],
                     "gastos_diarios": 900.0},
            "Guadalajara": {"hoteles": ["Grand Fiesta Americana", "Hyatt Regency", "Sheraton"],
                           "actividades": ["Centro Histórico", "Hospicio Cabañas", "Laguna de Chapala"],
                           "gastos_diarios": 700.0}
        }

        if destino not in destinos:
            print(f"Destino no disponible. Usando Cancún por defecto.")
            destino = "Cancún"

        datos_destino = destinos[destino]

        # Generar itinerario
        print(f"Itinerario para {dias} días en {destino} con presupuesto de ${presupuesto:.2f} MXN")
        print(f"Gasto diario estimado: ${datos_destino['gastos_diarios']:.2f} MXN")
        print(f"Presupuesto total estimado: ${dias * datos_destino['gastos_diarios']:.2f} MXN")

        print("\nItinerario sugerido:")
        for dia in range(1, dias + 1):
            hotel = random.choice(datos_destino["hoteles"])
            actividad = random.choice(datos_destino["actividades"])
            print(f"Día {dia}: Alojamiento en {hotel} - Actividad: {actividad}")

        print(f"\nTotal estimado: ${dias * datos_destino['gastos_diarios']:.2f} MXN")

    except Exception as e:
        print(f"Error al generar itinerario: {str(e)}")
        print("Ejemplo de uso: python generador_itinerario_viaje.py Cancún 7 15000.0")

if __name__ == "__main__":
    main()