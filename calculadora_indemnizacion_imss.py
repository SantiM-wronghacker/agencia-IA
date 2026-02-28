"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza calculadora de indemnización IMSS
TECNOLOGÍA: Python estándar
"""

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_indemnizacion(salario_diario, anos_trabajados):
    """Calcula la indemnización IMSS según la ley mexicana con ajustes por antigüedad."""
    if anos_trabajados < 0:
        raise ValueError("Años trabajados no pueden ser negativos")
    if anos_trabajados < 1:
        return 0

    # Ajuste por antigüedad (20% adicional por cada año después del primero)
    factor_antiguedad = 1 + min(0.2, 0.02 * (anos_trabajados - 1))

    if anos_trabajados <= 15:
        return salario_diario * 90 * anos_trabajados * factor_antiguedad
    else:
        primera_parte = salario_diario * 90 * 15 * factor_antiguedad
        segunda_parte = salario_diario * 20 * (anos_trabajados - 15) * factor_antiguedad
        return primera_parte + segunda_parte

def main():
    try:
        if len(sys.argv) < 3:
            salario_diario = 500  # Default: salario mínimo en México (2023)
            anos_trabajados = 5   # Default: 5 años
        else:
            salario_diario = float(sys.argv[1])
            anos_trabajados = float(sys.argv[2])

        if salario_diario <= 0:
            raise ValueError("Salario diario debe ser mayor a cero")
        if anos_trabajados < 0:
            raise ValueError("Años trabajados no pueden ser negativos")

        indemnizacion = calcular_indemnizacion(salario_diario, anos_trabajados)

        print("=== CALCULADORA DE INDEMNIZACIÓN IMSS ===")
        print(f"Salario diario: ${salario_diario:.2f} MXN")
        print(f"Años trabajados: {anos_trabajados:.1f} años")
        print(f"Indemnización base: ${indemnizacion:.2f} MXN")
        print(f"Indemnización mensual: ${indemnizacion / 30:.2f} MXN")
        print(f"Indemnización anual: ${indemnizacion * 12 / 30:.2f} MXN")
        print(f"Indemnización diaria: ${indemnizacion / 30:.2f} MXN")
        print(f"Factor de antigüedad aplicado: {1 + min(0.2, 0.02 * (anos_trabajados - 1)):.2f}x")
        print(f"Límite máximo de indemnización: ${salario_diario * 90 * 15 * 1.2:.2f} MXN (15 años con 20% adicional)")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"Para {anos_trabajados:.1f} años de servicio con salario diario de ${salario_diario:.2f} MXN:")
        print(f"La indemnización total calculada es de ${indemnizacion:.2f} MXN")
        print(f"Esto representa aproximadamente ${indemnizacion / 30:.2f} MXN mensuales")
        print(f"Se recomienda verificar con un abogado laboral para casos especiales")

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()