"""
ÁREA: LEGAL
DESCRIPCIÓN: Agente que realiza generador carta poder
TECNOLOGÍA: Python estándar
"""
import sys
import os
import json
import datetime
import random
import math

def main():
    try:
        # Parámetros por defecto
        nombre_representante = sys.argv[1] if len(sys.argv) > 1 else "Juan Pérez García"
        nombre_cliente = sys.argv[2] if len(sys.argv) > 2 else "María López Martínez"
        fecha = sys.argv[3] if len(sys.argv) > 3 else datetime.date.today().strftime("%d/%m/%Y")
        rfc = sys.argv[4] if len(sys.argv) > 4 else "PEJU800101"
        monto = float(sys.argv[5]) if len(sys.argv) > 5 else 150000.00
        iva = 0.16  # IVA para México
        isr = 0.10  # ISR para México

        # Validar parámetros
        if not isinstance(monto, (int, float)) or monto <= 0:
            raise ValueError("El monto debe ser un número positivo")

        # Generar carta poder
        carta_poder = f"""
        CARTA PODER

        Por medio de la presente, yo {nombre_cliente}, con RFC {rfc}, otorgo poder amplio y suficiente
        a {nombre_representante} para que me represente en todos los actos jurídicos y administrativos
        relacionados con el monto de ${monto:.2f} MXN, en la Ciudad de México, a {fecha}.

        Atentamente,
        {nombre_cliente}
        """

        # Calcular impuestos
        iva_monto = monto * iva
        isr_monto = monto * isr
        total_monto = monto + iva_monto + isr_monto

        # Guardar en archivo
        filename = f"carta_poder_{nombre_cliente.replace(' ', '_')}.txt"
        with open(filename, 'w') as f:
            f.write(carta_poder)

        print("Carta poder generada exitosamente.")
        print(f"Nombre del representante: {nombre_representante}")
        print(f"Nombre del cliente: {nombre_cliente}")
        print(f"Fecha: {fecha}")
        print(f"RFC: {rfc}")
        print(f"Monto: ${monto:.2f} MXN")
        print(f"IVA (16%): ${iva_monto:.2f} MXN")
        print(f"ISR (10%): ${isr_monto:.2f} MXN")
        print(f"Total: ${total_monto:.2f} MXN")
        print(f"Archivo guardado como: {filename}")
        print("Resumen ejecutivo:")
        print(f"Se ha generado una carta poder para {nombre_cliente} con un monto de ${monto:.2f} MXN,")
        print(f"con un total de ${total_monto:.2f} MXN incluyendo impuestos.")

    except ValueError as e:
        print(f"Error de validación: {str(e)}")
    except Exception as e:
        print(f"Error al generar la carta poder: {str(e)}")

if __name__ == "__main__":
    main()