# HERRAMIENTAS/Validador de formato RFC Mexico/Python

import sys
import re
import datetime

def main():
    try:
        rfc = sys.argv[1] if len(sys.argv) > 1 else "PEM180101HTCSDN09"
        patron = re.compile(r'^[A-Z]{4}\d{6}[A-Z0-9]{3}$')
        if patron.match(rfc):
            print("RFC:", rfc)
            print("Fecha de nacimiento:", rfc[4:6], "/", rfc[6:8], "/", "19" + rfc[8:10] if rfc[8:10] > "50" else "20" + rfc[8:10])
            print("Lugar de nacimiento:", obtener_lugar_nacimiento(rfc[11]))
            print("Tipo de persona:", "Fisica" if rfc[10] in "0123456789" else "Moral")
            print("Homoclave:", rfc[9])
        else:
            print("RFC no valido")
    except Exception as e:
        print("Error:", str(e))

def obtener_lugar_nacimiento(clave):
    lugares = {
        "0": "Ciudad de Mexico",
        "1": "Aguascalientes",
        "2": "Baja California",
        "3": "Baja California Sur",
        "4": "Campeche",
        "5": "Chiapas",
        "6": "Chihuahua",
        "7": "Coahuila",
        "8": "Colima",
        "9": "Durango",
        "10": "Guanajuato",
        "11": "Guerrero",
        "12": "Hidalgo",
        "13": "Jalisco",
        "14": "Estado de Mexico",
        "15": "Michoacan",
        "16": "Morelos",
        "17": "Nayarit",
        "18": "Nuevo Leon",
        "19": "Oaxaca",
        "20": "Puebla",
        "21": "Queretaro",
        "22": "Quintana Roo",
        "23": "San Luis Potosi",
        "24": "Sinaloa",
        "25": "Sonora",
        "26": "Tabasco",
        "27": "Tamaulipas",
        "28": "Tlaxcala",
        "29": "Veracruz",
        "30": "Yucatan",
        "31": "Zacatecas",
        "32": "Nacido en el extranjero"
    }
    return lugares.get(clave, "Desconocido")

if __name__ == '__main__':
    main()