import json
import os
import sys
import subprocess
import time

def cargar_habilidades():
    try:
        with open('habilidades.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error al cargar habilidades.json: {e}")
        return {}

def mostrar_menu():
    habilidades = cargar_habilidades()
    if not habilidades:
        print("No hay agentes mapeados. Ejecuta primero mapeador_capacidades.py")
        return

    categorias = {}
    for archivo, info in habilidades.items():
        cat = info.get('categoria', 'Otros')
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append((archivo, info))

    print("\n" + "="*60)
    print("        HUB CENTRAL DE AGENTES - AGENCIA SANTI")
    print("="*60)

    indice_global = 1
    mapeo_opciones = {}

    for cat in sorted(categorias.keys()):
        print(f"\nAREA: {cat.upper()}")
        print("-" * 30)
        for archivo, info in categorias[cat]:
            desc = info.get('descripcion', 'Sin descripción')
            salud = info.get('salud', 'OK')
            tecno = ", ".join(info.get('tecnologia', []))
            
            estado = "[RED]" if "Requiere" in salud else "[OK]"
            
            print(f"{indice_global}. {archivo:<35} {estado}")
            print(f"   {desc[:65]}...")
            if tecno: print(f"   Tech: {tecno}")
            
            mapeo_opciones[str(indice_global)] = archivo
            indice_global += 1

    print("\n" + "="*60)
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
    else:
        print("No se proporciono un agente para ejecutar. Salir.")
        sys.exit()

    if opcion in mapeo_opciones:
        archivo_elegido = mapeo_opciones[opcion]
        print(f"\nIniciando: {archivo_elegido}...")
        try:
            subprocess.run([sys.executable, archivo_elegido])
            time.sleep(2)
        except Exception as e:
            print(f"Error al ejecutar {archivo_elegido}: {e}")
    else:
        print("Opción no válida.")

if __name__ == "__main__":
    mostrar_menu()