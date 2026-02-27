"""
ÁREA: SEGUROS
DESCRIPCIÓN: Agente que realiza calculadora seguro vida mexico
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calcula_seguro_vida(edad, sexo, estado_civil, ingresos_mensuales, dependientes):
    prima_base = 800.0  # Ajustada según datos de México
    ajuste_edad = 0.05 * (edad - 25)
    ajuste_sexo = 0.1 if sexo == 'M' else -0.05
    ajuste_estado_civil = 0.05 if estado_civil == 'C' else 0.0
    ajuste_ingresos = 0.01 * (ingresos_mensuales / 15000.0)  # Ajustada según ingresos promedio en México
    ajuste_dependientes = 0.05 * dependientes
    prima = prima_base + ajuste_edad + ajuste_sexo + ajuste_estado_civil + ajuste_ingresos + ajuste_dependientes
    return prima

def main():
    try:
        edad = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        sexo = sys.argv[2] if len(sys.argv) > 2 else 'M'
        estado_civil = sys.argv[3] if len(sys.argv) > 3 else 'S'
        ingresos_mensuales = int(sys.argv[4]) if len(sys.argv) > 4 else 25000
        dependientes = int(sys.argv[5]) if len(sys.argv) > 5 else 2
        prima = calcula_seguro_vida(edad, sexo, estado_civil, ingresos_mensuales, dependientes)
        print(f'Datos del asegurado:')
        print(f'Edad: {edad} años')
        print(f'Sexo: {sexo}')
        print(f'Estado civil: {estado_civil}')
        print(f'Ingresos mensuales: ${ingresos_mensuales:,.2f} MXN')
        print(f'Dependientes: {dependientes} personas')
        print(f'\nResumen de costos:')
        print(f'Prima del seguro de vida: ${prima:,.2f} MXN')
        print(f'Prima anual del seguro de vida: ${prima * 12:,.2f} MXN')
        print(f'Prima mensual del seguro de vida con IVA (16%): ${prima * 1.16:,.2f} MXN')
        print(f'Prima anual del seguro de vida con IVA (16%): ${prima * 12 * 1.16:,.2f} MXN')
        print(f'\nResumen ejecutivo:')
        print(f'El costo del seguro de vida para una persona de {edad} años, sexo {sexo}, estado civil {estado_civil}, con ingresos mensuales de ${ingresos_mensuales:,.2f} MXN y {dependientes} dependientes, es de ${prima:,.2f} MXN al mes.')
        print(f'Es importante considerar que este cálculo es una estimación y puede variar según la aseguradora y otras condiciones.')
    except ValueError as e:
        print(f'Error: {str(e)}')
        print('Por favor, ingrese valores numéricos para edad, ingresos mensuales y dependientes.')
    except IndexError:
        print('Error: Faltan parámetros.')
        print('Uso: python calculadora_seguro_vida_mexico.py <edad> <sexo> <estado_civil> <ingresos_mensuales> <dependientes>')

if __name__ == "__main__":
    main()