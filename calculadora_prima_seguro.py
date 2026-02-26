"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza calculadora prima seguro
TECNOLOGÍA: Python estándar
"""
import sys
import math

def calcular_prima(edad, monto_asegurado, tipo_vehiculo):
    # Parámetros base para México
    base_anual = 0.03  # 3% base
    factor_edad = 1.0
    factor_vehiculo = 1.0

    # Ajustes por edad
    if edad < 25:
        factor_edad = 1.5
    elif edad < 30:
        factor_edad = 1.3
    elif edad > 65:
        factor_edad = 1.2

    # Ajustes por tipo de vehículo
    if tipo_vehiculo.lower() == "lujo":
        factor_vehiculo = 1.8
    elif tipo_vehiculo.lower() == "suv":
        factor_vehiculo = 1.4
    elif tipo_vehiculo.lower() == "economico":
        factor_vehiculo = 0.9

    prima_anual = monto_asegurado * base_anual * factor_edad * factor_vehiculo
    prima_mensual = prima_anual / 12

    return {
        "prima_anual": round(prima_anual, 2),
        "prima_mensual": round(prima_mensual, 2),
        "factor_edad": factor_edad,
        "factor_vehiculo": factor_vehiculo
    }

def main():
    try:
        # Valores por defecto realistas para México
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 35
        monto_asegurado = float(sys.argv[2]) if len(sys.argv) > 2 else 300000.00
        tipo_vehiculo = sys.argv[3] if len(sys.argv) > 3 else "economico"

        resultado = calcular_prima(edad, monto_asegurado, tipo_vehiculo)

        print("Cálculo de prima de seguro de auto")
        print(f"Edad del asegurado: {edad} años")
        print(f"Monto asegurado: ${monto_asegurado:,.2f} MXN")
        print(f"Tipo de vehículo: {tipo_vehiculo}")
        print(f"Prima anual: ${resultado['prima_anual']:,.2f} MXN")
        print(f"Prima mensual: ${resultado['prima_mensual']:,.2f} MXN")
        print(f"Factor por edad: {resultado['factor_edad']:.2f}x")
        print(f"Factor por vehículo: {resultado['factor_vehiculo']:.2f}x")

    except Exception as e:
        print(f"Error en el cálculo: {str(e)}")
        print("Uso: python calculadora_prima_seguro.py [edad] [monto_asegurado] [tipo_vehiculo]")
        print("Ejemplo: python calculadora_prima_seguro.py 35 300000 economico")

if __name__ == "__main__":
    main()