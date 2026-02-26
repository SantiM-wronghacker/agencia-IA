"""
AREA: HERRAMIENTAS
DESCRIPCION: Agente de tarea Celery con Redis como Broker y Backend
TECNOLOGIA: Celery, Redis, Python
"""
from celery import Celery
import time
import sys
import json

def configure_celery_app(broker_url, backend_url, task_name):
    try:
        celery_app = Celery(task_name, 
                            broker=broker_url, 
                            backend=backend_url)
        celery_app.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            task_track_started=True,
            task_time_limit=300, 
        )
        return celery_app
    except Exception as e:
        print(f"Error configurando Celery App: {str(e)}")
        return None

def main():
    if len(sys.argv) < 3:
        print("Uso: python celery_app.py <broker_url> <backend_url> <task_name>")
        return

    broker_url = sys.argv[1]
    backend_url = sys.argv[2]
    task_name = sys.argv[3]

    celery_app = configure_celery_app(broker_url, backend_url, task_name)

    if celery_app is not None:
        print("Celery App configurada y lista para recibir tareas.")
        print(f"Broker URL: {broker_url}")
        print(f"Backend URL: {backend_url}")
        print(f"Task Name: {task_name}")
        print(f"Task Serializer: {celery_app.conf.task_serializer}")
        print(f"Accept Content: {celery_app.conf.accept_content}")
        print(f"Result Serializer: {celery_app.conf.result_serializer}")
        print(f"Timezone: {celery_app.conf.timezone}")
        print(f"Enable UTC: {celery_app.conf.enable_utc}")
        print(f"Task Track Started: {celery_app.conf.task_track_started}")
        print(f"Task Time Limit: {celery_app.conf.task_time_limit} segundos")
        time.sleep(2)
        print("Resumen Ejecutivo:")
        print(f"Celery App configurada con éxito. Broker URL: {broker_url}, Backend URL: {backend_url}, Task Name: {task_name}")

if __name__ == "__main__":
    main()