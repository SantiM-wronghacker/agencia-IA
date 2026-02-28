"""
ÁREA: RESTAURANTES
DESCRIPCIÓN: Agente que realiza generador menu precios
TECNOLOGÍA: Python estándar
"""

import sys
import json
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Configuración por defecto
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        platos = ["Tacos al pastor", "Enchiladas verdes", "Pozole rojo", "Mole de pollo", "Chilaquiles"]
        precios_base = [55, 70, 85, 95, 60]
        impuestos = 0.16  # IVA

        # Parámetros configurables
        dia = sys.argv[1] if len(sys.argv) > 1 else random.choice(dias_semana)
        descuento = float(sys.argv[2]) if len(sys.argv) > 2 else random.uniform(0, 0.2)

        # Generar menú con precios
        menu = []
        total_ventas = 0
        total_descuentos = 0
        for plato, precio in zip(platos, precios_base):
            precio_final = precio * (1 - descuento) * (1 + impuestos)
            menu.append({
                "plato": plato,
                "precio_original": precio,
                "precio_final": round(precio_final, 2),
                "descuento": f"{descuento*100:.1f}%"
            })
            total_ventas += precio_final
            total_descuentos += precio * descuento

        # Generar salida
        print(f"MENÚ DEL DÍA: {dia.upper()}")
        print(f"FECHA: {datetime.now().strftime('%d/%m/%Y')}")
        print("PLATO\t\tPRECIO\tDESCUENTO")
        for item in menu:
            print(f"{item['plato']}\t${item['precio_final']:.2f}\t{item['descuento']}")
        print(f"TOTAL VENTAS: ${total_ventas:.2f}")
        print(f"TOTAL DESCUENTOS: ${total_descuentos:.2f}")
        print(f"IMPUESTOS (IVA {impuestos*100:.0f}%): ${total_ventas - sum(item['precio_final'] for item in menu):.2f}")

        # Resumen ejecutivo
        print("\nRESUMEN EJECUTIVO:")
        print(f"Día: {dia}")
        print(f"Total ventas: ${total_ventas:.2f}")
        print(f"Total descuentos: ${total_descuentos:.2f}")
        print(f"Utilidad neta: ${total_ventas - total_descuentos:.2f}")

        # Guardar en JSON
        with open(f"menu_{dia.lower()}.json", "w") as f:
            json.dump(menu, f, indent=2)

    except IndexError:
        print("Error: Debe proporcionar el día y el descuento como argumentos", file=sys.stderr)
        sys.exit(1)
    except ValueError:
        print("Error: El descuento debe ser un número", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()