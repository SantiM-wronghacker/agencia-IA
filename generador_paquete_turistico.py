"""
ÁREA: TURISMO
DESCRIPCIÓN: Agente que realiza generador paquete turistico
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

def generar_paquete(destinos=None, actividades=None, precios=None):
    if destinos is None:
        destinos = ["Cancún", "Los Cabos", "Puerto Vallarta", "Riviera Maya", "Guadalajara"]
    if actividades is None:
        actividades = ["Excursión a ruinas mayas", "Tour gastronómico", "Buceo en arrecifes", "Visita a parques naturales", "Experiencia cultural"]
    if precios is None:
        precios = [1500, 2200, 2800, 3500, 4200]

    destino = random.choice(destinos)
    actividad = random.choice(actividades)
    precio = random.choice(precios)
    dias = random.randint(3, 7)
    fecha_salida = datetime.now() + timedelta(days=random.randint(7, 30))

    return {
        "destino": destino,
        "actividad": actividad,
        "precio": precio,
        "dias": dias,
        "fecha_salida": fecha_salida.strftime("%Y-%m-%d")
    }

def calcular_impuestos(precio):
    iva = 0.16
    isr = 0.10
    return precio * iva + precio * isr

def calcular_total(precio, impuestos):
    return precio + impuestos

def main():
    try:
        if len(sys.argv) > 1:
            destinos = sys.argv[1].split(",")
            actividades = sys.argv[2].split(",")
            precios = [int(x) for x in sys.argv[3].split(",")]
        else:
            destinos = None
            actividades = None
            precios = None

        paquete = generar_paquete(destinos, actividades, precios)
        impuestos = calcular_impuestos(paquete['precio'])
        total = calcular_total(paquete['precio'], impuestos)

        print("Paquete turístico generado:")
        print(f"Destino: {paquete['destino']}")
        print(f"Actividad principal: {paquete['actividad']}")
        print(f"Precio por persona: ${paquete['precio']} MXN")
        print(f"Impuestos (IVA e ISR): ${impuestos:.2f} MXN")
        print(f"Total: ${total:.2f} MXN")
        print(f"Duración: {paquete['dias']} días")
        print(f"Fecha de salida: {paquete['fecha_salida']}")
        print(f"Fecha de regreso: {(datetime.strptime(paquete['fecha_salida'], '%Y-%m-%d') + timedelta(days=paquete['dias'])).strftime('%Y-%m-%d')}")
        print("Resumen ejecutivo:")
        print(f"El paquete turístico generado tiene un costo total de ${total:.2f} MXN por persona, con una duración de {paquete['dias']} días en {paquete['destino']}.")
    except Exception as e:
        print(f"Error al generar el paquete: {e}")

if __name__ == "__main__":
    main()