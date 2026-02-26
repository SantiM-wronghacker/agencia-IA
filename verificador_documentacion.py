"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Verifica la documentación requerida para procesos de renta
TECNOLOGÍA: Python
"""

import sys
import time

def verificar_documentacion(ine=False, comprobante=False, aval=False):
    print("Verificador de Documentación para Renta")
    print("-----------------------------------------")

    documentos = {
        "INE": ine,
        "Comprobante de Ingresos": comprobante,
        "Aval": aval
    }

    while True:
        print("\nDocumentos:")
        for documento, tiene in documentos.items():
            if tiene:
                print(f"- {documento}: Si")
            else:
                print(f"- {documento}: No")

        print("\n¿Qué deseas hacer?")
        print("1. Agregar documento")
        print("2. Quitar documento")
        print("3. Finalizar")

        accion = sys.argv[4] if len(sys.argv) > 4 else "3"

        if accion == "1":
            print("\n¿Qué documento deseas agregar?")
            print("1. INE")
            print("2. Comprobante de Ingresos")
            print("3. Aval")

            documento_agregar = sys.argv[5] if len(sys.argv) > 5 else "1"

            if documento_agregar == "1":
                documentos["INE"] = True
            elif documento_agregar == "2":
                documentos["Comprobante de Ingresos"] = True
            elif documento_agregar == "3":
                documentos["Aval"] = True
            else:
                print("Opción inválida. Por favor, selecciona una opción válida.")
        elif accion == "2":
            print("\n¿Qué documento deseas quitar?")
            print("1. INE")
            print("2. Comprobante de Ingresos")
            print("3. Aval")

            documento_quitar = sys.argv[5] if len(sys.argv) > 5 else "1"

            if documento_quitar == "1":
                documentos["INE"] = False
            elif documento_quitar == "2":
                documentos["Comprobante de Ingresos"] = False
            elif documento_quitar == "3":
                documentos["Aval"] = False
            else:
                print("Opción inválida. Por favor, selecciona una opción válida.")
        elif accion == "3":
            if all(tiene for tiene in documentos.values()):
                print("\nLa documentación está completa.")
            else:
                print("\nLa documentación no está completa. Por favor, asegúrate de tener todos los documentos necesarios.")

            break
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")

        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ine = sys.argv[1].lower() == "true"
        comprobante = sys.argv[2].lower() == "true"
        aval = sys.argv[3].lower() == "true"
    else:
        ine = False
        comprobante = False
        aval = False

    print(f"INE: {ine}, Comprobante de Ingresos: {comprobante}, Aval: {aval}")
    verificar_documentacion(ine, comprobante, aval)