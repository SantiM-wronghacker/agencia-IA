"""
AREA: FINANZAS
DESCRIPCION: Analiza flujo de caja mensual de un negocio. Recibe ingresos y egresos por categoría, calcula saldo neto, identifica meses críticos y proyecta 12 meses hacia adelante.
TECNOLOGIA: Python estándar
"""

import sys
import math

def main():
    try:
        if len(sys.argv) == 4:
            ingresos_mensuales = int(sys.argv[1])
            egresos_fijos = int(sys.argv[2])
            egresos_variables = int(sys.argv[3])
        else:
            ingresos_mensuales = 150000
            egresos_fijos = 80000
            egresos_variables = 30000

        saldo_neto = ingresos_mensuales - egresos_fijos - egresos_variables
        meses_criticos = 0
        proyeccion = []
        tasa_interes_anual = 0.06  # Tasa de interés anual para cálculo de intereses
        tasa_inflacion_anual = 0.03  # Tasa de inflación anual para cálculo de ajuste de precios

        for i in range(12):
            saldo_proyectado = saldo_neto * (i + 1)
            if saldo_proyectado < 0:
                meses_criticos += 1
            proyeccion.append(saldo_proyectado)

        # Cálculo de intereses y ajuste de precios
        intereses_mensuales = (ingresos_mensuales * tasa_interes_anual) / 12
        ajuste_precios_mensuales = (ingresos_mensuales * tasa_inflacion_anual) / 12

        print(f"Ingresos mensuales: {ingresos_mensuales}")
        print(f"Egresos fijos: {egresos_fijos}")
        print(f"Egresos variables: {egresos_variables}")
        print(f"Saldo neto: {saldo_neto}")
        print(f"Meses críticos: {meses_criticos}")
        print(f"Proyección 12 meses: {proyeccion}")
        print(f"Intereses mensuales: {intereses_mensuales}")
        print(f"Ajuste de precios mensuales: {ajuste_precios_mensuales}")
        print(f"Saldo neto con intereses y ajuste de precios: {saldo_neto + intereses_mensuales - ajuste_precios_mensuales}")
        print(f"Resumen ejecutivo: El negocio tiene un saldo neto de {saldo_neto} y se proyecta un total de {meses_criticos} meses críticos en los próximos 12 meses.")

    except ValueError as e:
        print(f"Error: {str(e)} - Por favor, ingrese valores numéricos.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()