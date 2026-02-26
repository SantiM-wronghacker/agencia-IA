"""
ÁREA: LEGAL
DESCRIPCIÓN: Genera acuerdos de confidencialidad (NDA) básicos para México. Recibe nombres de las partes, objeto del acuerdo y vigencia. Produce documento en texto listo para firmar.
TECNOLOGÍA: Python estándar
"""

import sys
from datetime import datetime, timedelta

def main():
    try:
        if len(sys.argv) == 5:
            parte_a = sys.argv[1]
            parte_b = sys.argv[2]
            objeto = sys.argv[3]
            vigencia_años = int(sys.argv[4])
        else:
            parte_a = 'Juan López'
            parte_b = 'Empresa XYZ'
            objeto = 'proyecto inmobiliario'
            vigencia_años = 2

        fecha_inicio = datetime.now().strftime("%d/%m/%Y")
        fecha_fin = (datetime.now() + timedelta(days=vigencia_años*365)).strftime("%d/%m/%Y")

        print(f"ACUERDO DE CONFIDENCIALIDAD ENTRE {parte_a} Y {parte_b}")
        print(f"OBJETO: {objeto}")
        print(f"VIGENCIA: {vigencia_años} años")
        print(f"FECHA DE INICIO: {fecha_inicio}")
        print(f"FECHA DE FIN: {fecha_fin}")
        print(f"LAS PARTES SE OBLIGAN A MANTENER CONFIDENCIALIDAD DURANTE {vigencia_años} AÑOS.")
        print(f"LAS PARTES SE OBLIGAN A NO DIVULGAR INFORMACIÓN CONFIDENCIAL A TERCEROS.")
        print(f"LAS PARTES SE OBLIGAN A PROTEGER LA INFORMACIÓN CONFIDENCIAL CON LA MISMA CUIDADO QUE PROTEGERÍAN SU PROPIA INFORMACIÓN CONFIDENCIAL.")
        print(f"LAS PARTES SE OBLIGAN A DEVOLVER TODA LA INFORMACIÓN CONFIDENCIAL AL FINALIZAR EL ACUERDO.")
        print(f"FIRMA DE {parte_a}: ______________________")
        print(f"FIRMA DE {parte_b}: ______________________")
        print(f"RESUMEN EJECUTIVO: El presente acuerdo de confidencialidad entre {parte_a} y {parte_b} tiene como objeto {objeto} y tendrá una vigencia de {vigencia_años} años, a partir de {fecha_inicio} y hasta {fecha_fin}.")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()