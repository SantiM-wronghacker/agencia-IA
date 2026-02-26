"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Clasificador de viviendas según su precio
TECNOLOGÍA: Python
"""

import sys
import time

class ClasificadorViviendas:
    def __init__(self, precio, ubicacion, tipo):
        self.precio = precio
        self.ubicacion = ubicacion
        self.tipo = tipo

    def clasificar(self):
        if self.precio < 200000:
            return 'Interes Social'
        elif self.precio < 500000:
            return 'Residencial'
        else:
            return 'Premium'

    def get_precio(self):
        return self.precio

    def set_precio(self, nuevo_precio):
        self.precio = nuevo_precio

    def get_ubicacion(self):
        return self.ubicacion

    def get_tipo(self):
        return self.tipo


def main():
    if len(sys.argv) > 3:
        precio = float(sys.argv[1])
        ubicacion = sys.argv[2]
        tipo = sys.argv[3]
    else:
        precio = 300000
        ubicacion = 'Ciudad de México'
        tipo = 'Departamento'
        print(f"Usando precio por defecto: {precio}, ubicación: {ubicacion}, tipo: {tipo}")

    try:
        clasificador = ClasificadorViviendas(precio, ubicacion, tipo)
        print(f"La propiedad se clasifica como: {clasificador.clasificar()}")
        print(f"Precio de la propiedad: {clasificador.get_precio()}")
        print(f"Ubicación de la propiedad: {clasificador.get_ubicacion()}")
        print(f"Tipo de propiedad: {clasificador.get_tipo()}")
        print(f"Fecha de clasificación: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Resumen ejecutivo: La propiedad ubicada en {clasificador.get_ubicacion()} con un precio de {clasificador.get_precio()} se clasifica como {clasificador.clasificar()}.")
        time.sleep(2)
    except ValueError:
        print("Error: El precio debe ser un número.")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()