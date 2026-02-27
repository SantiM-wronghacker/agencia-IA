import sys
import math

def main():
    try:
        if len(sys.argv) == 4:
            ingresos_mensuales = int(sys.argv[1])
            egresos_fijos = int(sys.argv[2])
            egresos_variables = int(sys.argv[3])
        else:
            ingresos_mensuales = 200000  # Ingresos mensuales promedio en México
            egresos_fijos = 120000  # Egresos fijos promedio en México
            egresos_variables = 40000  # Egresos variables promedio en México

        saldo_neto = ingresos_mensuales - egresos_fijos - egresos_variables
        meses_criticos = 0
        proyeccion = []
        tasa_interes_anual = 0.08  # Tasa de interés anual promedio en México
        tasa_inflacion_anual = 0.04  # Tasa de inflación anual promedio en México

        for i in range(12):
            saldo_proyectado = saldo_neto * (i + 1)
            if saldo_proyectado < 0:
                meses_criticos += 1
            proyeccion.append(saldo_proyectado)

        # Cálculo de intereses y ajuste de precios
        intereses_mensuales = (ingresos_mensuales * tasa_interes_anual) / 12
        ajuste_precios_mensuales = (ingresos_mensuales * tasa_inflacion_anual) / 12

        print(f"Ingresos mensuales: ${ingresos_mensuales:,.2f} MXN")
        print(f"Egresos fijos: ${egresos_fijos:,.2f} MXN")
        print(f"Egresos variables: ${egresos_variables:,.2f} MXN")
        print(f"Saldo neto: ${saldo_neto:,.2f} MXN")
        print(f"Meses críticos: {meses_criticos} meses")
        print(f"Proyección 12 meses: {proyeccion}")
        print(f"Intereses mensuales: ${intereses_mensuales:,.2f} MXN")
        print(f"Ajuste de precios mensuales: ${ajuste_precios_mensuales:,.2f} MXN")
        print(f"Saldo neto con intereses y ajuste de precios: ${saldo_neto + intereses_mensuales - ajuste_precios_mensuales:,.2f} MXN")
        print(f"Resumen ejecutivo: El negocio tiene un saldo neto de ${saldo_neto:,.2f} MXN y se proyecta un total de {meses_criticos} meses críticos en el próximo año. Es importante considerar los intereses mensuales y el ajuste de precios para tomar decisiones informadas.")
    except ValueError:
        print("Error: Los parámetros deben ser números enteros.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()