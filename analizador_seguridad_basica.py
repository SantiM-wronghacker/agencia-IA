"""
ÁREA: TECNOLOGÍA
DESCRIPCIÓN: Agente que realiza analizador seguridad basica
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import datetime
import math
import re
import random

def main():
    try:
        # Configuración predeterminada
        archivo = sys.argv[1] if len(sys.argv) > 1 else "seguridad.json"
        dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30

        # Verificar existencia del archivo
        if not os.path.exists(archivo):
            print(f"Error: Archivo {archivo} no encontrado")
            return

        # Leer datos de seguridad
        with open(archivo, 'r') as f:
            datos = json.load(f)

        # Análisis básico
        eventos = datos.get('eventos', [])
        eventos_recentes = [e for e in eventos if (datetime.datetime.now() - datetime.datetime.strptime(e['fecha'], '%Y-%m-%d')).days <= dias]

        # Estadísticas
        total_eventos = len(eventos)
        eventos_recentes_count = len(eventos_recentes)
        eventos_criticos = sum(1 for e in eventos_recentes if e['nivel'] == 'CRÍTICO')
        eventos_alta = sum(1 for e in eventos_recentes if e['nivel'] == 'ALTA')
        eventos_baja = sum(1 for e in eventos_recentes if e['nivel'] == 'BAJA')

        # Salida de resultados
        print("=== ANÁLISIS DE SEGURIDAD BÁSICO ===")
        print(f"Total eventos registrados: {total_eventos}")
        print(f"Eventos en últimos {dias} días: {eventos_recentes_count}")
        print(f"Eventos críticos recientes: {eventos_criticos}")
        print(f"Eventos de alta prioridad recientes: {eventos_alta}")
        print(f"Eventos de baja prioridad recientes: {eventos_baja}")

    except Exception as e:
        print(f"Error en el análisis: {str(e)}")

if __name__ == "__main__":
    main()