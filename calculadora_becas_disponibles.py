"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza calculadora becas disponibles
TECNOLOGÍA: Python estándar
"""
import sys
import random
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def main():
    try:
        # Parámetros por defecto
        if len(sys.argv) > 1:
            presupuesto = int(sys.argv[1])
            becas_por_estudiante = int(sys.argv[2])
            estudiantes_registrados = int(sys.argv[3])
        else:
            presupuesto = 15000000  # MXN
            becas_por_estudiante = 5000  # MXN
            estudiantes_registrados = 2000

        # Procesamiento
        if presupuesto <= 0 or becas_por_estudiante <= 0 or estudiantes_registrados <= 0:
            raise ValueError("Parámetros deben ser números positivos")

        becas_disponibles = presupuesto // becas_por_estudiante
        becas_otorgadas = min(estudiantes_registrados, becas_disponibles)
        presupuesto_restante = presupuesto - (becas_otorgadas * becas_por_estudiante)
        porcentaje_asignado = (becas_otorgadas / estudiantes_registrados) * 100
        porcentaje_presupuesto_asignado = (becas_otorgadas * becas_por_estudiante / presupuesto) * 100

        # Salida
        print("=== REPORTE DE BECAS DISPONIBLES ===")
        print(f"Presupuesto total: ${presupuesto:,.2f} MXN")
        print(f"Becas disponibles: {becas_disponibles:,} (${becas_por_estudiante:,.2f} c/u)")
        print(f"Estudiantes beneficiados: {becas_otorgadas:,} ({porcentaje_asignado:.1f}%)")
        print(f"Presupuesto restante: ${presupuesto_restante:,.2f} MXN")
        print(f"Porcentaje de presupuesto asignado: {porcentaje_presupuesto_asignado:.1f}%")
        print(f"Fecha de cálculo: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Estudiantes no beneficiados: {estudiantes_registrados - becas_otorgadas:,} ({100 - porcentaje_asignado:.1f}%)")
        print(f"Monto total de becas otorgadas: ${becas_otorgadas * becas_por_estudiante:,.2f} MXN")
        print("=== RESUMEN EJECUTIVO ===")
        print(f"Se han otorgado {becas_otorgadas:,} becas a estudiantes, lo que representa el {porcentaje_asignado:.1f}% del total de estudiantes registrados.")
        print(f"El monto total de becas otorgadas es de ${becas_otorgadas * becas_por_estudiante:,.2f} MXN, lo que representa el {porcentaje_presupuesto_asignado:.1f}% del presupuesto total.")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")

if __name__ == "__main__":
    main()