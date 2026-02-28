"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza calculadora costo carrera mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto realistas para México
        carrera = sys.argv[1] if len(sys.argv) > 1 else "Ingeniería"
        semestres = int(sys.argv[2]) if len(sys.argv) > 2 else 8
        costo_semestre = float(sys.argv[3]) if len(sys.argv) > 3 else 25000.0  # MXN
        costo_libros = float(sys.argv[4]) if len(sys.argv) > 4 else 2000.0  # MXN
        costo_transporte = float(sys.argv[5]) if len(sys.argv) > 5 else 1500.0  # MXN

        # Cálculos
        costo_total = costo_semestre * semestres
        costo_mensual = (costo_semestre / 5) + (costo_libros / 10) + (costo_transporte / 5)  # 5 meses por semestre
        costo_anual = (costo_semestre * 2) + (costo_libros * 2) + (costo_transporte * 10)  # 2 semestres por año
        costo_total_estimado = costo_total + (costo_libros * semestres) + (costo_transporte * semestres)

        # Output
        print("Cálculo de costo de carrera en México")
        print(f"Carrera: {carrera}")
        print(f"Costo por semestre: ${costo_semestre:,.2f} MXN")
        print(f"Costo total estimado: ${costo_total:,.2f} MXN")
        print(f"Costo mensual estimado: ${costo_mensual:,.2f} MXN")
        print(f"Costo anual estimado: ${costo_anual:,.2f} MXN")
        print(f"Costo de libros por semestre: ${costo_libros:,.2f} MXN")
        print(f"Costo de transporte por mes: ${costo_transporte:,.2f} MXN")
        print(f"Costo total estimado con gastos adicionales: ${costo_total_estimado:,.2f} MXN")
        print(f"Duración de la carrera: {semestres} semestres")
        print(f"Duración de la carrera en años: {semestres / 2} años")

        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"La carrera de {carrera} tiene un costo total estimado de ${costo_total_estimado:,.2f} MXN.")
        print(f"El costo mensual estimado es de ${costo_mensual:,.2f} MXN.")
        print(f"El costo anual estimado es de ${costo_anual:,.2f} MXN.")

    except IndexError:
        print("Error: Faltan parámetros.")
        print("Uso: python calculadora_costo_carrera_mexico.py [carrera] [semestres] [costo_semestre] [costo_libros] [costo_transporte]")
        print("Ejemplo: python calculadora_costo_carrera_mexico.py Medicina 10 30000 2000 1500")
    except ValueError:
        print("Error: Parámetros inválidos.")
        print("Uso: python calculadora_costo_carrera_mexico.py [carrera] [semestres] [costo_semestre] [costo_libros] [costo_transporte]")
        print("Ejemplo: python calculadora_costo_carrera_mexico.py Medicina 10 30000 2000 1500")
    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()