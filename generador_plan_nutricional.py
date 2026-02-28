"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza generador plan nutricional
TECNOLOGÍA: Python estándar
"""

import sys
import random
import datetime
import json

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def generar_plan_nutricional(edad, peso, altura, actividad):
    # Cálculo de IMC
    imc = peso / (altura ** 2)

    # Cálculo de TMB (Tasa Metabólica Basal)
    if actividad == "sedentario":
        tmb = 1.2
    elif actividad == "ligero":
        tmb = 1.375
    elif actividad == "moderado":
        tmb = 1.55
    else:
        tmb = 1.725

    tmb_calculada = (10 * peso) + (6.25 * altura * 100) - (5 * edad) + 5
    calorias_diarias = tmb_calculada * tmb

    # Generación de plan nutricional
    plan = {
        "desayuno": [
            {"alimento": "Huevos revueltos", "cantidad": "2 unidades", "calorias": 140},
            {"alimento": "Tortilla de maíz", "cantidad": "2 piezas", "calorias": 100},
            {"alimento": "Fresas", "cantidad": "100g", "calorias": 33}
        ],
        "comida": [
            {"alimento": "Pollo a la plancha", "cantidad": "150g", "calorias": 230},
            {"alimento": "Arroz integral", "cantidad": "100g", "calorias": 110},
            {"alimento": "Brócoli al vapor", "cantidad": "100g", "calorias": 35}
        ],
        "cena": [
            {"alimento": "Salmón al horno", "cantidad": "120g", "calorias": 250},
            {"alimento": "Quinoa", "cantidad": "80g", "calorias": 120},
            {"alimento": "Espinacas", "cantidad": "50g", "calorias": 12}
        ],
        "snacks": [
            {"alimento": "Yogur natural", "cantidad": "1 unidad", "calorias": 100},
            {"alimento": "Almendras", "cantidad": "10 unidades", "calorias": 70}
        ]
    }

    return {
        "imc": round(imc, 2),
        "tmb": round(tmb_calculada, 2),
        "calorias_diarias": round(calorias_diarias, 2),
        "plan_nutricional": plan
    }

def main():
    try:
        if len(sys.argv) < 5:
            edad = 30
            peso = 70
            altura = 1.75
            actividad = "moderado"
        else:
            edad = int(sys.argv[1])
            peso = float(sys.argv[2])
            altura = float(sys.argv[3])
            actividad = sys.argv[4]

        resultado = generar_plan_nutricional(edad, peso, altura, actividad)

        print(f"IMC: {resultado['imc']}")
        print(f"TMB: {resultado['tmb']} kcal/día")
        print(f"Calorías diarias recomendadas: {resultado['calorias_diarias']} kcal")
        print("\nPlan nutricional:")
        for comida, alimentos in resultado['plan_nutricional'].items():
            print(f"\n{comida.capitalize()}:")
            for alimento in alimentos:
                print(f"- {alimento['alimento']}: {alimento['cantidad']} ({alimento['calorias']} kcal)")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()