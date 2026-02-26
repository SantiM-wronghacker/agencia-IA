"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Calcula la plusvalía proyectada de una propiedad a 5 y 10 años según colonia, tipo de inmueble y tasa de crecimiento histórica de la zona en CDMX.
TECNOLOGÍA: Python estándar
"""

import sys
import math

def main():
    try:
        if len(sys.argv) < 4:
            precio_actual = 2000000
            colonia = "Polanco"
            tipo_inmueble = "departamento"
        else:
            precio_actual = float(sys.argv[1])
            colonia = sys.argv[2]
            tipo_inmueble = sys.argv[3]

        tasas_crecimiento = {
            "Polanco": 0.05,
            "Condesa": 0.04,
            "Roma": 0.03,
            "Juárez": 0.02,
        }

        if colonia not in tasas_crecimiento:
            tasa_crecimiento = 0.03
        else:
            tasa_crecimiento = tasas_crecimiento[colonia]

        plusvalia_5_anos = precio_actual * (1 + tasa_crecimiento) ** 5 - precio_actual
        plusvalia_10_anos = precio_actual * (1 + tasa_crecimiento) ** 10 - precio_actual

        print(f"Datos de la propiedad:")
        print(f"  - Colonia: {colonia}")
        print(f"  - Tipo de inmueble: {tipo_inmueble}")
        print(f"  - Precio actual: ${precio_actual:.2f}")
        print(f"  - Tasa de crecimiento histórica: {tasa_crecimiento*100}%")
        print(f"Proyecciones de plusvalía:")
        print(f"  - Plusvalía proyectada a 5 años: ${plusvalia_5_anos:.2f}")
        print(f"  - Plusvalía proyectada a 10 años: ${plusvalia_10_anos:.2f}")
        print(f"  - Incremento porcentual a 5 años: {(plusvalia_5_anos/precio_actual)*100:.2f}%")
        print(f"  - Incremento porcentual a 10 años: {(plusvalia_10_anos/precio_actual)*100:.2f}%")
        print(f"Resumen ejecutivo:")
        print(f"  - La propiedad en {colonia} tiene un potencial de crecimiento de {tasa_crecimiento*100}% anual.")
        print(f"  - En 5 años, se proyecta un incremento de ${plusvalia_5_anos:.2f} y en 10 años de ${plusvalia_10_anos:.2f}.")
        print(f"  - Es importante considerar que estas proyecciones son estimaciones y pueden variar según el mercado y otros factores.")

    except ValueError as e:
        print(f"Error: El precio actual debe ser un número. {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()