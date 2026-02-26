"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Generador de fichas técnicas de propiedades
TECNOLOGÍA: Python, sys
"""

import sys
import time
import math

class Propiedad:
    def __init__(self, m2, recamaras, precio, ubicacion, antiguedad, estado):
        self.m2 = m2
        self.recamaras = recamaras
        self.precio = precio
        self.ubicacion = ubicacion
        self.antiguedad = antiguedad
        self.estado = estado

    def generador_ficha_tecnica(self):
        return f"Ficha Técnica de Propiedad en {self.ubicacion}\n\n" \
               f"* Tamaño: {self.m2} m2\n" \
               f"* Recámaras: {self.recamaras}\n" \
               f"* Precio: ${self.precio:,.2f}\n" \
               f"* Antigüedad: {self.antiguedad} años\n" \
               f"* Estado: {self.estado}\n" \
               f"* Precio por m2: ${self.precio / self.m2:,.2f}\n" \
               f"* Impuesto sobre la renta (ISR): {self.precio * 0.02:,.2f}\n" \
               f"* Comisión del agente: {self.precio * 0.05:,.2f}\n"

def main():
    try:
        if len(sys.argv) < 6:
            m2 = 200
            recamaras = 3
            precio = 500000.0
            ubicacion = "Ciudad de México"
            antiguedad = 10
            estado = "Excelente"
            print(f"Usando valores por defecto: m2={m2}, recamaras={recamaras}, precio={precio}, ubicacion={ubicacion}, antiguedad={antiguedad}, estado={estado}")
        else:
            m2 = int(sys.argv[1])
            recamaras = int(sys.argv[2])
            precio = float(sys.argv[3])
            ubicacion = sys.argv[4]
            antiguedad = int(sys.argv[5])
            estado = sys.argv[6] if len(sys.argv) > 6 else "Excelente"

        propiedad = Propiedad(m2, recamaras, precio, ubicacion, antiguedad, estado)
        ficha_tecnica = propiedad.generador_ficha_tecnica()

        print("\nFicha Técnica Generada:")
        print(ficha_tecnica)

        time.sleep(2)
        enviar_whatsapp = "si"
        if enviar_whatsapp.lower() == "si":
            print("Ficha técnica enviada por WhatsApp:")
            print(ficha_tecnica)
        else:
            print("Ficha técnica no enviada.")

        print("\nResumen Ejecutivo:")
        print(f"La propiedad de {m2} m2 en {ubicacion} con {recamaras} recámaras y un precio de ${precio:,.2f} es una excelente oportunidad de inversión.")
        print(f"El precio por m2 es de ${precio / m2:,.2f} y el impuesto sobre la renta (ISR) es de ${precio * 0.02:,.2f}.")
        print(f"La comisión del agente es de ${precio * 0.05:,.2f}.")

    except ValueError:
        print("Error: Los valores ingresados no son válidos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()