"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Evalúa una zona o colonia de CDMX para inversión inmobiliaria. Analiza plusvalía, seguridad, servicios, demanda de renta y emite un score de 1 a 10 con recomendación.
TECNOLOGÍA: Python estándar
"""

import sys
import json
import math

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

def evaluar_zona(colonia, presupuesto):
    try:
        # Plusvalía
        plusvalia = {
            "Polanco": 0.07,
            "Condesa": 0.05,
            "Roma": 0.04,
            "Juárez": 0.03,
            "Cuauhtémoc": 0.02
        }.get(colonia, 0.01)
        
        # Seguridad
        seguridad = {
            "Polanco": 9,
            "Condesa": 8,
            "Roma": 7,
            "Juárez": 6,
            "Cuauhtémoc": 5
        }.get(colonia, 4)
        
        # Servicios
        servicios = {
            "Polanco": 9,
            "Condesa": 8,
            "Roma": 7,
            "Juárez": 6,
            "Cuauhtémoc": 5
        }.get(colonia, 4)
        
        # Demanda de renta
        demanda_renta = {
            "Polanco": 8,
            "Condesa": 7,
            "Roma": 6,
            "Juárez": 5,
            "Cuauhtémoc": 4
        }.get(colonia, 3)
        
        # Score
        score = (plusvalia * 25 + seguridad * 25 + servicios * 20 + demanda_renta * 30) / 100
        score = math.ceil(score * 10)
        
        # Recomendación
        if score >= 8:
            recomendacion = "Invierta"
        elif score >= 5:
            recomendacion = "Considere"
        else:
            recomendacion = "No invierta"
        
        return score, recomendacion, plusvalia, seguridad, servicios, demanda_renta
    
    except Exception as e:
        return None, str(e), None, None, None, None

def main():
    if len(sys.argv) < 3:
        colonia = "Polanco"
        presupuesto = 2000000
    else:
        colonia = sys.argv[1]
        presupuesto = int(sys.argv[2])
    
    score, recomendacion, plusvalia, seguridad, servicios, demanda_renta = evaluar_zona(colonia, presupuesto)
    
    if score is not None:
        print(f"Colonia: {colonia}")
        print(f"Presupuesto: {presupuesto}")
        print(f"Plusvalía: {plusvalia*100}%")
        print(f"Seguridad: {seguridad}/10")
        print(f"Servicios: {servicios}/10")
        print(f"Demanada de renta: {demanda_renta}/10")
        print(f"Score: {score}/10")
        print(f"Recomendación: {recomendacion}")
        print("\nResumen Ejecutivo:")
        print(f"La colonia {colonia} tiene un score de {score}/10, con una plusvalía del {plusvalia*100}% y una demanda de renta de {demanda_renta}/10.")
        print(f"Se recomienda {recomendacion} en esta zona.")
    else:
        print(f"Error: {recomendacion}")

if __name__ == "__main__":
    main()