"""
ÁREA: EDUCACIÓN
DESCRIPCIÓN: Agente que realiza generador ejercicios practica
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

def generar_ejercicios(cantidad=5, temas=None, niveles=None):
    if temas is None:
        temas = ["matemáticas", "español", "historia", "ciencias", "geografía"]
    if niveles is None:
        niveles = ["primaria", "secundaria", "preparatoria"]
    
    ejercicios = []
    for _ in range(cantidad):
        tema = random.choice(temas)
        nivel = random.choice(niveles)
        fecha = datetime.date.today().strftime("%d/%m/%Y")
        ejercicios.append({
            "tema": tema,
            "nivel": nivel,
            "fecha": fecha,
            "ejercicio": f"Ejercicio de {tema} para {nivel} - {random.randint(1, 10)} problemas",
            "duracion": f"{random.randint(30, 90)} minutos",
            "dificultad": random.choice(["baja", "media", "alta"]),
            "objetivos": [
                f"Comprender conceptos básicos de {tema}",
                f"Desarrollar habilidades de resolución de problemas en {tema}",
                f"Aplicar conocimientos de {tema} en situaciones reales"
            ],
            "materiales": [
                f"Libro de texto de {tema}",
                f"Cuaderno y lápiz",
                f"Calculadora"
            ]
        })

    return ejercicios

def main():
    try:
        if len(sys.argv) > 1:
            cantidad = int(sys.argv[1])
        else:
            cantidad = 5
        if len(sys.argv) > 2:
            temas = sys.argv[2].split(",")
        else:
            temas = None
        if len(sys.argv) > 3:
            niveles = sys.argv[3].split(",")
        else:
            niveles = None
        ejercicios = generar_ejercicios(cantidad, temas, niveles)
        for idx, ejercicio in enumerate(ejercicios, 1):
            print(f"{idx}. Tema: {ejercicio['tema']}, Nivel: {ejercicio['nivel']}, Fecha: {ejercicio['fecha']}, Ejercicio: {ejercicio['ejercicio']}, Duración: {ejercicio['duracion']}, Dificultad: {ejercicio['dificultad']}")
            print(f"  Objetivos: {', '.join(ejercicio['objetivos'])}")
            print(f"  Materiales: {', '.join(ejercicio['materiales'])}")
        print("\nResumen Ejecutivo:")
        print(f"Total de ejercicios generados: {len(ejercicios)}")
        print(f"Temas cubiertos: {set([e['tema'] for e in ejercicios])}")
        print(f"Niveles cubiertos: {set([e['nivel'] for e in ejercicios])}")
        print(f"Duración total estimada: {sum([int(e['duracion'].split(' ')[0]) for e in ejercicios])} minutos")
        print(f"Dificultad promedio: {sum([['baja', 'media', 'alta'].index(e['dificultad']) for e in ejercicios]) / len(ejercicios)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()