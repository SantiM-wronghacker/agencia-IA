"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza analizador cuellos botella
TECNOLOGÍA: Python estándar
"""
import sys
import json
import random
from datetime import datetime

def main():
    try:
        # Parámetros por defecto
        dias = int(sys.argv[1]) if len(sys.argv) > 1 else 30
        umbral = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8

        # Simulación de datos de producción diaria (en unidades)
        datos_produccion = [random.randint(100, 500) for _ in range(dias)]

        # Análisis de cuellos de botella
        promedios_moviles = []
        for i in range(dias - 6):
            ventana = datos_produccion[i:i+7]
            promedios_moviles.append(sum(ventana) / 7)

        # Identificación de cuellos de botella
        cuellos_botella = []
        for i, promedio in enumerate(promedios_moviles):
            if promedio < umbral * max(datos_produccion):
                cuellos_botella.append({
                    'dia': i + 1,
                    'promedio': round(promedio, 2),
                    'produccion': datos_produccion[i]
                })

        # Reporte
        print(f"Análisis de cuellos de botella (últimos {dias} días)")
        print(f"Fecha de análisis: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print(f"Total días analizados: {dias}")
        print(f"Días con cuellos de botella: {len(cuellos_botella)}")
        print(f"Producción promedio en cuellos de botella: {sum(c[1] for c in cuellos_botella)/len(cuellos_botella) if cuellos_botella else 0:.2f} unidades")

        if cuellos_botella:
            print("\nDetalle de cuellos de botella:")
            for item in cuellos_botella[:3]:  # Mostrar solo los primeros 3 para no saturar
                print(f"  Día {item['dia']}: {item['produccion']} unidades (promedio móvil: {item['promedio']})")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()