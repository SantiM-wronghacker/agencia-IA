"""
ÁREA: RECURSOS HUMANOS
DESCRIPCIÓN: Agente que genera descripciones detalladas de puestos con cálculos fiscales y laborales precisos para México
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def calcular_isr(sueldo_anual):
    """Cálculo del ISR anual según tabla 2023 México"""
    if sueldo_anual <= 758.75:
        return sueldo_anual * 0.0192
    elif sueldo_anual <= 1046.08:
        return 14.45 + (sueldo_anual - 758.75) * 0.064
    elif sueldo_anual <= 1379.88:
        return 47.73 + (sueldo_anual - 1046.08) * 0.08
    elif sueldo_anual <= 1654.54:
        return 81.73 + (sueldo_anual - 1379.88) * 0.103
    elif sueldo_anual <= 2137.21:
        return 136.98 + (sueldo_anual - 1654.54) * 0.12
    elif sueldo_anual <= 3205.82:
        return 246.98 + (sueldo_anual - 2137.21) * 0.142
    elif sueldo_anual <= 4537.14:
        return 444.21 + (sueldo_anual - 3205.82) * 0.164
    elif sueldo_anual <= 9726.81:
        return 719.68 + (sueldo_anual - 4537.14) * 0.179
    elif sueldo_anual <= 12968.47:
        return 1485.96 + (sueldo_anual - 9726.81) * 0.2136
    elif sueldo_anual <= 24185.57:
        return 2331.83 + (sueldo_anual - 12968.47) * 0.2352
    elif sueldo_anual <= 37658.32:
        return 4693.53 + (sueldo_anual - 24185.57) * 0.3
    elif sueldo_anual <= 72349.50:
        return 9381.13 + (sueldo_anual - 37658.32) * 0.32
    elif sueldo_anual <= 97268.10:
        return 19136.73 + (sueldo_anual - 72349.50) * 0.34
    else:
        return 27063.93 + (sueldo_anual - 97268.10) * 0.35

def calcular_imss(sueldo_anual):
    """Cálculo de IMSS anual con tope máximo"""
    umbral = 25 * 730.55  # 25 UMA 2023
    if sueldo_anual > umbral:
        sueldo_anual = umbral
    return sueldo_anual * 0.05

def calcular_infonavit(sueldo_anual):
    """Cálculo de INFONAVIT anual con tope máximo"""
    umbral = 25 * 730.55  # 25 UMA 2023
    if sueldo_anual > umbral:
        sueldo_anual = umbral
    return su