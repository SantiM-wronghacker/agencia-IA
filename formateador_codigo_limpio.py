"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Formateador de código que revisa la indentación y docstrings en archivos .py
TECNOLOGÍA: Python, ast
"""
import ast
import os
import sys
import time

def revisar_indentacion(codigo):
    try:
        ast.parse(codigo)
        return True
    except IndentationError:
        return False

def revisar_docstrings(codigo):
    arbol = ast.parse(codigo)
    funciones = [n for n in arbol.body if isinstance(n, ast.FunctionDef)]
    for func in funciones:
        if not func.body or not isinstance(func.body[0], ast.Expr) or not isinstance(func.body[0].value, ast.Str):
            return False
    return True

def formatear_codigo(ruta_archivo):
    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()
    except UnicodeDecodeError:
        print(f"Error al leer el archivo {ruta_archivo}. Es posible que tenga caracteres no soportados.")
        return False
    
    if not revisar_indentacion(codigo):
        print(f"El archivo {ruta_archivo} tiene problemas de indentación.")
        return False
    
    if not revisar_docstrings(codigo):
        print(f"El archivo {ruta_archivo} no tiene docstrings en sus funciones.")
        return False
    
    print(f"El archivo {ruta_archivo} está bien formateado.")
    return True

def main():
    ruta_actual = os.getcwd()
    if len(sys.argv) > 1:
        for archivo in sys.argv[1:]:
            if archivo.endswith(".py"):
                if archivo != os.path.basename(__file__):  
                    formatear_codigo(archivo)
    else:
        print("Usando valores por defecto")
        for archivo in os.listdir(ruta_actual):
            if archivo.endswith(".py"):
                if archivo != os.path.basename(__file__):  
                    formatear_codigo(archivo)

if __name__ == "__main__":
    main()