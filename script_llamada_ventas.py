"""
ÁREA: VENTAS
DESCRIPCIÓN: Genera scripts de llamada de ventas personalizados para diferentes tipos de prospectos. Incluye apertura, manejo de objeciones y cierre según el perfil del cliente.
TECNOLOGÍA: Python estándar
"""

import sys

def generar_script(tipo_prospecto, producto):
    try:
        script = f"Script de llamada para {tipo_prospecto} interesado en {producto}:\n"
        script += "Apertura: Hola, ¿cómo estás? Me llamo Juan y soy asesor de ventas.\n"
        script += "Manejo de objeciones: ¿Cuál es tu principal preocupación al considerar la compra de un {0}?\n".format(producto)
        script += "Cierre: ¿Qué te parece si agendamos una cita para discutir más a fondo tus necesidades y cómo podemos ayudarte a encontrar el {0} perfecto?\n".format(producto)
        script += "Detalles del producto: El {0} es un producto de alta calidad que ofrece {1} características y beneficios.\n".format(producto, obtener_caracteristicas(producto))
        script += "Beneficios del producto: Al adquirir nuestro {0}, podrás disfrutar de {1} beneficios y ventajas.\n".format(producto, obtener_beneficios(producto))
        return script
    except Exception as e:
        return f"Error: {str(e)}"

def obtener_caracteristicas(producto):
    try:
        caracteristicas = {
            "departamento_polanco": "amplios espacios, excelente ubicación y acabados de lujo",
            "casa_hacienda": "jardines amplios, piscina y áreas de recreación",
            "oficina_centro": "excelente ubicación, fácil acceso y seguridad las 24 horas"
        }
        return caracteristicas.get(producto, "no disponible")
    except Exception as e:
        return f"Error: {str(e)}"

def obtener_beneficios(producto):
    try:
        beneficios = {
            "departamento_polanco": "seguridad, comodidad y acceso a servicios de alta calidad",
            "casa_hacienda": "espacio, libertad y conexión con la naturaleza",
            "oficina_centro": "visibilidad, accesibilidad y oportunidades de negocio"
        }
        return beneficios.get(producto, "no disponible")
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    if len(sys.argv) < 3:
        tipo_prospecto = "inversionista"
        producto = "departamento_polanco"
    else:
        tipo_prospecto = sys.argv[1]
        producto = sys.argv[2]
    print(generar_script(tipo_prospecto, producto))
    print("\nResumen Ejecutivo:")
    print("Tipo de prospecto:", tipo_prospecto)
    print("Producto:", producto)
    print("Características del producto:", obtener_caracteristicas(producto))
    print("Beneficios del producto:", obtener_beneficios(producto))

if __name__ == "__main__":
    main()