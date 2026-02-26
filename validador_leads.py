"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Validador de leads para agencia inmobiliaria que clasifica clientes según presupuesto y urgencia
TECNOLOGÍA: Python
"""

import sys
import time

class Lead:
    def __init__(self, nombre, presupuesto, urgencia):
        self.nombre = nombre
        self.presupuesto = presupuesto
        self.urgencia = urgencia

    def calificar_leads(self):
        if self.presupuesto < 10000 and self.urgencia == "baja":
            return "Frio"
        elif (self.presupuesto >= 10000 and self.presupuesto < 50000) and (self.urgencia == "media" or self.urgencia == "baja"):
            return "Tibio"
        elif self.presupuesto >= 50000 and self.urgencia == "alta":
            return "Caliente"
        elif self.presupuesto >= 50000 and (self.urgencia == "media" or self.urgencia == "baja"):
            return "Tibio"
        elif self.presupuesto < 10000 and self.urgencia == "alta":
            return "Tibio"
        else:
            return "Frio"

class ValidadorLeads:
    def __init__(self):
        self.leads = []

    def agregar_lead(self, nombre, presupuesto, urgencia):
        lead = Lead(nombre, presupuesto, urgencia)
        self.leads.append(lead)

    def calificar_leads(self):
        for lead in self.leads:
            calificacion = lead.calificar_leads()
            print(f"Nombre: {lead.nombre}, Presupuesto: ${lead.presupuesto:,.2f}, Urgencia: {lead.urgencia}, Calificacion: {calificacion}")

def main():
    if len(sys.argv) > 1:
        try:
            nombre = sys.argv[1]
            presupuesto = float(sys.argv[2])
            urgencia = sys.argv[3].lower()
            if urgencia not in ["alta", "media", "baja"]:
                urgencia = "media"
        except (ValueError, IndexError):
            print("Error: Parámetros incorrectos. Usando valores por defecto.")
            nombre = "Cliente"
            presupuesto = 50000
            urgencia = "media"
    else:
        print("No se proporcionaron argumentos. Usando valores por defecto para México:")
        print("Presupuesto: $50,000.00 | Urgencia: media")
        nombre = "Cliente"
        presupuesto = 50000
        urgencia = "media"

    validador = ValidadorLeads()
    validador.agregar_lead(nombre, presupuesto, urgencia)
    time.sleep(2)
    validador.calificar_leads()

if __name__ == "__main__":
    main()