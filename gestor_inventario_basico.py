"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza gestor inventario basico
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Configuración por defecto
        archivo_inventario = "inventario.json"
        cantidad_articulos = 10
        precio_promedio = 150.50
        fecha_actual = datetime.now().strftime("%Y-%m-%d")

        # Procesamiento de argumentos
        if len(sys.argv) > 1:
            archivo_inventario = sys.argv[1]
        if len(sys.argv) > 2:
            cantidad_articulos = int(sys.argv[2])
        if len(sys.argv) > 3:
            precio_promedio = float(sys.argv[3])

        # Generar datos de inventario
        inventario = []
        for i in range(1, cantidad_articulos + 1):
            articulo = {
                "id": f"ART-{random.randint(1000, 9999)}",
                "nombre": f"Producto {i}",
                "cantidad": random.randint(1, 100),
                "precio": round(precio_promedio * random.uniform(0.8, 1.2), 2),
                "fecha_registro": fecha_actual
            }
            inventario.append(articulo)

        # Guardar en archivo
        with open(archivo_inventario, "w") as f:
            json.dump(inventario, f, indent=2)

        # Mostrar resultados
        print(f"Inventario generado con {len(inventario)} artículos")
        print(f"Fecha de generación: {fecha_actual}")
        print(f"Precio promedio: ${precio_promedio:.2f} MXN")
        print(f"Artículo más caro: ${max(item['precio'] for item in inventario):.2f} MXN")
        print(f"Artículo más barato: ${min(item['precio'] for item in inventario):.2f} MXN")
        print(f"Total en inventario: ${sum(item['precio'] * item['cantidad'] for item in inventario):.2f} MXN")

    except Exception as e:
        print(f"Error en el procesamiento: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()