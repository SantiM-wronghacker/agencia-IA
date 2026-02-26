"""
ÁREA: OPERACIONES
DESCRIPCIÓN: Agente que realiza generador procedimientos sop
TECNOLOGÍA: Python estándar
"""

import sys
import os
import json
import random
from datetime import datetime, timedelta

def main():
    try:
        # Configuración por defecto
        dias = 30
        clientes = 10
        monto_min = 500
        monto_max = 5000

        # Procesar argumentos
        if len(sys.argv) > 1:
            dias = int(sys.argv[1])
        if len(sys.argv) > 2:
            clientes = int(sys.argv[2])

        # Generar datos de procedimientos
        procedimientos = []
        for i in range(clientes):
            fecha = (datetime.now() - timedelta(days=random.randint(0, dias))).strftime('%Y-%m-%d')
            monto = round(random.uniform(monto_min, monto_max), 2)
            procedimientos.append({
                "id": f"PROC-{i+1:04d}",
                "fecha": fecha,
                "cliente": f"CLIENTE-{i+1:03d}",
                "monto": monto,
                "status": random.choice(["PENDIENTE", "APROBADO", "RECHAZADO"])
            })

        # Guardar en archivo JSON
        output_file = "procedimientos_sop.json"
        with open(output_file, 'w') as f:
            json.dump(procedimientos, f, indent=4)

        # Mostrar resumen
        print(f"Generador de procedimientos SOP - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Clientes procesados: {clientes}")
        print(f"Rango de fechas: últimos {dias} días")
        print(f"Montos generados: entre ${monto_min} y ${monto_max} MXN")
        print(f"Archivo generado: {os.path.abspath(output_file)}")
        print("Procedimientos generados:")
        for proc in procedimientos[:3]:  # Mostrar solo 3 ejemplos
            print(f"  {proc['id']}: {proc['cliente']} - ${proc['monto']} ({proc['status']})")

    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()