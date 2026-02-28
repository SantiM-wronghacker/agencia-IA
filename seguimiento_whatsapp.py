"""
ÁREA: REAL ESTATE
DESCRIPCIÓN: Agente de seguimiento de clientes que envía recordatorios mediante WhatsApp
TECNOLOGÍA: Python, SQLite, Twilio
"""

import datetime
import sqlite3
from twilio.rest import Client
import time

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

# Configuración de la base de datos
DATABASE_NAME = 'clientes.db'

# Configuración de Twilio
ACCOUNT_SID = 'tu_account_sid'
AUTH_TOKEN = 'tu_auth_token'
CLIENT_TWILIO = Client(ACCOUNT_SID, AUTH_TOKEN)
FROM_NUMBER = 'tu_numero_twilio'

def crear_tabla_clientes():
    conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS clientes
                 (id INTEGER PRIMARY KEY, nombre TEXT, telefono TEXT, fecha_registro DATE)''')
    conn.commit()
    conn.close()

def agregar_cliente(nombre, telefono):
    conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
    c = conn.cursor()
    c.execute("INSERT INTO clientes (nombre, telefono, fecha_registro) VALUES (?, ?, ?)",
              (nombre, telefono, datetime.date.today()))
    conn.commit()
    conn.close()

def obtener_clientes():
    conn = sqlite3.connect(DATABASE_NAME, encoding='utf-8')
    c = conn.cursor()
    c.execute("SELECT * FROM clientes")
    clientes = c.fetchall()
    conn.close()
    return clientes

def enviar_recordatorio(telefono, mensaje):
    message = CLIENT_TWILIO.messages.create(
        body=mensaje,
        from_=FROM_NUMBER,
        to=telefono
    )
    time.sleep(2)

def generar_recordatorios():
    clientes = obtener_clientes()
    hoy = datetime.date.today()
    for cliente in clientes:
        id, nombre, telefono, fecha_registro = cliente
        dias_transcurridos = (hoy - fecha_registro).days
        if dias_transcurridos == 3:
            mensaje = f"Hola {nombre}, ¡esperamos que estés satisfecho con nuestro servicio! ¿Necesitas algo más?"
            enviar_recordatorio(telefono, mensaje)
            print(f"Recordatorio enviado a {nombre} después de {dias_transcurridos} días")
        elif dias_transcurridos == 7:
            mensaje = f"Hola {nombre}, ¿cómo te sientes con nuestro servicio hasta ahora? ¿Hay algo en lo que podamos ayudarte?"
            enviar_recordatorio(telefono, mensaje)
            print(f"Recordatorio enviado a {nombre} después de {dias_transcurridos} días")
        elif dias_transcurridos == 15:
            mensaje = f"Hola {nombre}, ¡esperamos que hayas encontrado lo que buscabas! ¿Qué podemos hacer para mejorar?"
            enviar_recordatorio(telefono, mensaje)
            print(f"Recordatorio enviado a {nombre} después de {dias_transcurridos} días")

if __name__ == "__main__":
    crear_tabla_clientes()
    agregar_cliente("Juan Pérez", "+56912345678")
    agregar_cliente("María Rodríguez", "+56990123456")
    generar_recordatorios()