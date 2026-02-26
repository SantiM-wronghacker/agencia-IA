"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente que realiza validador datos entrada
TECNOLOGÍA: Python estándar
"""

import sys
import json
import datetime
import math
import re
import random

def main():
    try:
        # Validación de argumentos
        if len(sys.argv) < 4:
            raise ValueError("Número de argumentos incorrecto. Se necesitan al menos 4 argumentos: nombre, edad, direccion y estado")
        
        # Asignación de argumentos
        nombre = sys.argv[1]
        edad = int(sys.argv[2])
        direccion = sys.argv[3]
        estado = sys.argv[4] if len(sys.argv) > 4 else "Mexico"
        
        # Validación de edad
        if edad < 0:
            raise ValueError("Edad no puede ser negativa")
        
        # Validación de dirección
        patron = re.compile(r"^(Calle|Avenida|Privada) [a-zA-Z0-9 ]+, [0-9]+, [a-zA-Z ]+, [a-zA-Z ]+$")
        if not patron.match(direccion):
            raise ValueError("Dirección no cumple con el formato esperado")
        
        # Generación de datos aleatorios
        cp = random.randint(10000, 99999)
        telefono = random.randint(1000000000, 9999999999)
        fecha_nacimiento = datetime.date.today() - datetime.timedelta(days=edad*365)
        
        # Cálculo de la edad en años, meses y días
        anos = edad
        meses = 0
        dias = 0
        if edad > 0:
            anos = edad // 12
            meses = (edad % 12)
        
        # Impresión de resultados
        print(f"Nombre: {nombre}")
        print(f"Edad: {anos} años, {meses} meses")
        print(f"Dirección: {direccion}, {estado}")
        print(f"Código Postal: {cp}")
        print(f"Teléfono: {telefono}")
        print(f"Fecha de Nacimiento: {fecha_nacimiento.strftime('%d/%m/%Y')}")
        print(f"Estado: {estado}")
        print(f"País: Mexico")
        print(f"Continente: América del Norte")
        
        # Resumen ejecutivo
        print("\nResumen Ejecutivo:")
        print(f"El usuario {nombre} tiene {anos} años y {meses} meses de edad.")
        print(f"Su dirección es {direccion}, {estado}, con código postal {cp}.")
        print(f"Su teléfono es {telefono} y su fecha de nacimiento es {fecha_nacimiento.strftime('%d/%m/%Y')}.")
    
    except ValueError as e:
        print(f"Error de valor: {str(e)}")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()