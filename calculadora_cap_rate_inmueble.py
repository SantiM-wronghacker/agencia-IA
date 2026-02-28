# REAL ESTATE / Calculadora cap rate inmueble / Python
# AREA: REAL ESTATE
# DESCRIPCION: Agente que realiza calculadora cap rate inmueble
# TECNOLOGIA: Python

import sys
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcula_cap_rate(precio_venta, ingresos_anuales, gastos_anuales):
    cap_rate = ((ingresos_anuales - gastos_anuales) / precio_venta) * 100
    return cap_rate

def calcula_rentabilidad_anual(ingresos_anuales, gastos_anuales):
    return ingresos_anuales - gastos_anuales

def calcula_tasa_de_retorno(precio_venta, rentabilidad_anual):
    return (rentabilidad_anual / precio_venta) * 100

def calcula_margen_de_beneficio(ingresos_anuales, gastos_anuales):
    return (ingresos_anuales - gastos_anuales) / ingresos_anuales * 100

def calcula_relacion_entre_ingresos_y_gastos(ingresos_anuales, gastos_anuales):
    if gastos_anuales == 0:
        return "No hay gastos anuales"
    else:
        return ingresos_anuales / gastos_anuales

def calcula_tasa_de_ocupacion(ingresos_anuales, precio_venta):
    return (ingresos_anuales / precio_venta) * 100

def main():
    try:
        precio_venta = float(sys.argv[1]) if len(sys.argv) > 1 else 5000000.0
        ingresos_anuales = float(sys.argv[2]) if len(sys.argv) > 2 else 120000.0
        gastos_anuales = float(sys.argv[3]) if len(sys.argv) > 3 else 30000.0

        cap_rate = calcula_cap_rate(precio_venta, ingresos_anuales, gastos_anuales)
        rentabilidad_anual = calcula_rentabilidad_anual(ingresos_anuales, gastos_anuales)
        tasa_de_retorno = calcula_tasa_de_retorno(precio_venta, rentabilidad_anual)
        margen_de_beneficio = calcula_margen_de_beneficio(ingresos_anuales, gastos_anuales)
        relacion_entre_ingresos_y_gastos = calcula_relacion_entre_ingresos_y_gastos(ingresos_anuales, gastos_anuales)
        tasa_de_ocupacion = calcula_tasa_de_ocupacion(ingresos_anuales, precio_venta)

        print(f"Precio de venta: ${precio_venta:,.2f} MXN")
        print(f"Ingresos anuales: ${ingresos_anuales:,.2f} MXN")
        print(f"Gastos anuales: ${gastos_anuales:,.2f} MXN")
        print(f"Cap Rate: {cap_rate:.2f}%")
        print(f"Rentabilidad anual: ${rentabilidad_anual:,.2f} MXN")
        print(f"Tasa de retorno: {tasa_de_retorno:.2f}%")
        print(f"Margen de beneficio: {margen_de_beneficio:.2f}%")
        print(f"Relación entre ingresos y gastos: {relacion_entre_ingresos_y_gastos}")
        print(f"Tasa de ocupación: {tasa_de_ocupacion:.2f}%")
        print(f"Resumen ejecutivo: La propiedad tiene un cap rate de {cap_rate:.2f}%, una rentabilidad anual de ${rentabilidad_anual:,.2f} MXN y una tasa de retorno de {tasa_de_retorno:.2f}%")
        print(f"Conclusión: La propiedad es {'' if cap_rate > 8 else 'no '}rentable")
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except ZeroDivisionError as e:
        print(f"Error de división por cero: {str(e)}")
    except Exception as e:
        print(f"Error desconocido: {str(e)}")

if __name__ == "__main__":
    main()