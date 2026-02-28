"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Gestiona y evalúa proveedores de servicios para una empresa. Registra nombre, servicio, costo mensual, calificación y genera ranking con recomendación de renovar o cambiar.
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_iva(costo_mensual):
    return costo_mensual * 0.16

def calcular_total(costo_mensual, iva):
    return costo_mensual + iva

def main():
    try:
        if len(sys.argv) == 1:
            proveedores = [
                {"nombre": "Proveedor 1", "servicio": "Internet", "costo_mensual": 500, "calificacion": 4},
                {"nombre": "Proveedor 2", "servicio": "Telefono", "costo_mensual": 300, "calificacion": 3},
                {"nombre": "Proveedor 3", "servicio": "Electricidad", "costo_mensual": 800, "calificacion": 5},
                {"nombre": "Proveedor 4", "servicio": "Agua", "costo_mensual": 200, "calificacion": 4},
                {"nombre": "Proveedor 5", "servicio": "Gas", "costo_mensual": 400, "calificacion": 3}
            ]
        else:
            proveedores = json.loads(sys.argv[1])
        
        proveedores.sort(key=lambda x: x["calificacion"], reverse=True)
        
        print("Ranking de proveedores:")
        for i, proveedor in enumerate(proveedores):
            iva = calcular_iva(proveedor["costo_mensual"])
            total = calcular_total(proveedor["costo_mensual"], iva)
            print(f"{i+1}. {proveedor['nombre']} - {proveedor['servicio']}:")
            print(f"  Costo mensual: ${proveedor['costo_mensual']:.2f}")
            print(f"  IVA (16%): ${iva:.2f}")
            print(f"  Total: ${total:.2f}")
            print(f"  Calificación: {proveedor['calificacion']}")
            if proveedor["calificacion"] >= 4:
                print("  Recomendación: Renovar")
            else:
                print("  Recomendación: Cambiar")
            print(f"  Fecha de evaluación: {datetime.date.today()}")
            print()
    
        print("Resumen ejecutivo:")
        print(f"Fecha de evaluación: {datetime.date.today()}")
        print(f"Número de proveedores evaluados: {len(proveedores)}")
        print(f"Proveedor con mayor calificación: {proveedores[0]['nombre']} - {proveedores[0]['servicio']}")
        print(f"Proveedor con menor calificación: {proveedores[-1]['nombre']} - {proveedores[-1]['servicio']}")
    
    except json.JSONDecodeError as e:
        print(f"Error: No se pudo decodificar el JSON - {e}")
    except KeyError as e:
        print(f"Error: No se encontró la clave - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()