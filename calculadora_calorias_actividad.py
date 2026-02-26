"""
ÁREA: SALUD
DESCRIPCIÓN: Agente que realiza calculadora calorias actividad
TECNOLOGÍA: Python estándar
"""
import sys
import math

def calcular_calorias(edad, peso, altura, actividad, tiempo):
    """Calcula calorias quemadas en actividad física."""
    if actividad == "caminar":
        met = 3.5
    elif actividad == "correr":
        met = 8.0
    elif actividad == "nadar":
        met = 6.0
    elif actividad == "ciclismo":
        met = 7.0
    else:
        met = 4.0

    calorias = (met * peso * tiempo) / 200
    return round(calorias, 2)

def calcular_calorias_basal(peso, altura, edad):
    """Calcula calorias basales."""
    calorias_basal = 66 + (6.2 * peso) + (12.7 * altura) - (6.8 * edad)
    return round(calorias_basal, 2)

def main():
    try:
        if len(sys.argv) < 6:
            edad = 30
            peso = 70  # kg
            altura = 170  # cm
            actividad = "caminar"
            tiempo = 30  # minutos
        else:
            edad = int(sys.argv[1])
            peso = float(sys.argv[2])
            altura = float(sys.argv[3])
            actividad = sys.argv[4]
            tiempo = float(sys.argv[5])

        calorias = calcular_calorias(edad, peso, altura, actividad, tiempo)
        calorias_basal = calcular_calorias_basal(peso, altura, edad)

        print("=== REPORTE DE CALORÍAS ===")
        print(f"Peso: {peso} kg")
        print(f"Altura: {altura} cm")
        print(f"Edad: {edad} años")
        print(f"Actividad: {actividad}")
        print(f"Tiempo: {tiempo} minutos")
        print(f"Calorías quemadas: {calorias} kcal")
        print(f"Calorías basales: {calorias_basal} kcal")
        print(f"Recomendación de consumo calórico diario: {calorias_basal * 1.2} kcal")
        print(f"Recomendación de hidratación: Beber al menos 2 litros de agua al día")
        print("Recomendación: Realizar ejercicio físico moderado al menos 3 veces a la semana")
        print("Recomendación: Dormir entre 7 y 9 horas diarias")
        print("Recomendación: Realizar chequeos médicos regulares")

        print("\n=== RESUMEN EJECUTIVO ===")
        print(f"El paciente de {edad} años, con un peso de {peso} kg y una altura de {altura} cm,")
        print(f"quemó {calorias} kcal realizando {actividad} durante {tiempo} minutos.")
        print(f"Se recomienda un consumo calórico diario de {calorias_basal * 1.2} kcal y")
        print(f"beber al menos 2 litros de agua al día.")

    except Exception as e:
        print(f"Error: {str(e)}")
        print("Uso: python calculadora_calorias_actividad.py [edad] [peso] [altura] [actividad] [tiempo]")
        print("Ejemplo: python calculadora_calorias_actividad.py 30 70 170 correr 45")

if __name__ == "__main__":
    main()