"""
ÁREA: FINANZAS
DESCRIPCIÓN: Agente que realiza cálculo de impuesto sobre la renta mensual con parámetros realistas para México
TECNOLOGÍA: Python estándar
"""

import sys
import math

def calculo_impuesto(renta_mensual, deducciones, isr_anterior=0):
    # Tablas de ISR 2023 para México (simplificadas)
    if renta_mensual <= 7333.33:
        tarifa = 0.0192
        limite_inferior = 0.0
        excedente = 0.0
    elif renta_mensual <= 10552.33:
        tarifa = 0.064
        limite_inferior = 7333.33
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 14965.97:
        tarifa = 0.1088
        limite_inferior = 10552.33
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 18805.91:
        tarifa = 0.16
        limite_inferior = 14965.97
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 25920.36:
        tarifa = 0.1792
        limite_inferior = 18805.91
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 38195.55:
        tarifa = 0.2136
        limite_inferior = 25920.36
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 73333.33:
        tarifa = 0.2352
        limite_inferior = 38195.55
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 97666.67:
        tarifa = 0.30
        limite_inferior = 73333.33
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 129800.00:
        tarifa = 0.32
        limite_inferior = 97666.67
        excedente = renta_mensual - limite_inferior
    elif renta_mensual <= 161933.33:
        tarifa = 0.34
        limite_inferior = 129800.00
        excedente = renta_mensual - limite_inferior
    else:
        tarifa = 0.35
        limite_inferior = 161933.33
        excedente = renta_mensual - limite_inferior

    # Cálculo del ISR
    cuota_fija = 0.0
    if renta_mensual > 7333.33:
        if renta_mensual <= 10552.33:
            cuota_fija = 140.88
        elif renta_mensual <= 14965.97:
            cuota_fija = 516.58
        elif renta_mensual <= 18805.91:
            cuota_fija = 923.68
        elif renta_mensual <= 25920.36:
            cuota_fija = 1485.58
        elif renta_mensual <= 38195.55:
            cuota_fija = 3157.07
        elif renta_mensual <= 73333.33:
            cuota_fija = 7603.53
        elif renta_mensual <= 97666.67:
            cu