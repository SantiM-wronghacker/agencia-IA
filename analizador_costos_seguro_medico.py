"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza analizador costos seguro medico
TECNOLOGÍA: Python estándar
"""
import sys
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Parámetros por defecto
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 35
        cobertura = sys.argv[2] if len(sys.argv) > 2 else "familiar"
        hospitales = int(sys.argv[3]) if len(sys.argv) > 3 else 3

        # Costos base en MXN (datos reales aproximados)
        costos_base = {
            "individual": 3500,
            "familiar": 6500,
            "ejecutivo": 12000
        }

        # Ajuste por edad
        if edad < 18:
            factor_edad = 0.8
        elif edad < 30:
            factor_edad = 0.95
        elif edad < 50:
            factor_edad = 1.0
        else:
            factor_edad = 1.2

        # Ajuste por hospitales
        factor_hospitales = 1 + (0.1 * (hospitales - 1))

        # Costo total
        costo_base = costos_base.get(cobertura, costos_base["familiar"])
        costo_total = round(costo_base * factor_edad * factor_hospitales, 2)

        # Generar datos adicionales
        fecha_actual = datetime.now().strftime("%Y-%m-%d")
        fecha_vencimiento = (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        deducible = random.randint(5000, 15000)
        copago = random.randint(100, 300)

        # Imprimir resultados
        print(f"Análisis de costo de seguro médico - {fecha_actual}")
        print(f"Cobertura: {cobertura.capitalize()}")
        print(f"Edad del titular: {edad} años")
        print(f"Costo mensual estimado: ${costo_total:,.2f} MXN")
        print(f"Deducible anual: ${deducible:,.2f} MXN")
        print(f"Copago por consulta: ${copago:,.2f} MXN")
        print(f"Vigencia hasta: {fecha_vencimiento}")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()