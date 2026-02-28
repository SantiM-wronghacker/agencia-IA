import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# AREA: FINANZAS
# DESCRIPCION: Analiza flujo de caja mensual de un negocio. Recibe ingresos y egresos por categoría, calcula saldo neto, identifica meses críticos y proyecta 12 meses hacia adelante.
# TECNOLOGIA: Python

def main():
    try:
        if len(sys.argv) == 7:
            ingresos_mensuales = int(sys.argv[1])
            egresos_fijos = int(sys.argv[2])
            egresos_variables = int(sys.argv[3])
            tasa_interes_anual = float(sys.argv[4])
            tasa_inflacion_anual = float(sys.argv[5])
            meses_proyeccion = int(sys.argv[6])
        else:
            ingresos_mensuales = 200000  # Ingresos mensuales promedio en México
            egresos_fijos = 120000  # Egresos fijos promedio en México
            egresos_variables = 40000  # Egresos variables promedio en México
            tasa_interes_anual = 0.08  # Tasa de interés anual promedio en México
            tasa_inflacion_anual = 0.04  # Tasa de inflación anual promedio en México
            meses_proyeccion = 12

        saldo_neto = ingresos_mensuales - egresos_fijos - egresos_variables
        meses_criticos = 0
        proyeccion = []
        intereses_mensuales = (ingresos_mensuales * tasa_interes_anual) / 12
        ajuste_precios_mensuales = (ingresos_mensuales * tasa_inflacion_anual) / 12

        for i in range(meses_proyeccion):
            saldo_proyectado = saldo_neto * (i + 1)
            if saldo_proyectado < 0:
                meses_criticos += 1
            proyeccion.append(saldo_proyectado)

        print(f"Ingresos mensuales: ${ingresos_mensuales:,.2f} MXN")
        print(f"Egresos fijos: ${egresos_fijos:,.2f} MXN")
        print(f"Egresos variables: ${egresos_variables:,.2f} MXN")
        print(f"Saldo neto: ${saldo_neto:,.2f} MXN")
        print(f"Meses críticos: {meses_criticos} meses")
        print(f"Proyección {meses_proyeccion} meses: {proyeccion}")
        print(f"Intereses mensuales: ${intereses_mensuales:,.2f} MXN")
        print(f"Ajuste de precios mensuales: ${ajuste_precios_mensuales:,.2f} MXN")
        print(f"Saldo neto con intereses y ajuste de precios: ${saldo_neto + intereses_mensuales - ajuste_precios_mensuales:,.2f} MXN")
        print(f"Resumen ejecutivo: El negocio tiene un saldo neto de ${saldo_neto:,.2f} MXN y se proyecta un total de {meses_criticos} meses críticos en el próximo año.")
        print(f"Recomendaciones:")
        print(f"  - Aumentar ingresos en un {((egresos_fijos + egresos_variables) - ingresos_mensuales) / ingresos_mensuales * 100:.2f}%")
        print(f"  - Reducir egresos fijos en un {((egresos_fijos / ingresos_mensuales) * 100):.2f}%")
        print(f"  - Reducir egresos variables en un {((egresos_variables / ingresos_mensuales) * 100):.2f}%")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()