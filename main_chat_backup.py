"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente de chat mejorado que utiliza la API de Groq para generar respuestas a preguntas del usuario
TECNOLOGÍA: Python, requests, json, Groq API
"""
import requests
import json
import sys
import time
from datetime import datetime

try:
    import web_bridge as web
    WEB = web.WEB  # True si hay conexion a internet
except ImportError:
    WEB = False

MODEL = "llama-3.3-70b-versatile"
API_URL = "https://api.groq.com/v1/models/" + MODEL + "/generate"
LOG_FILE = "log.txt"
DEFAULT_PROMPT = "Eres un asistente útil, directo y práctico.\nTú: "

def get_api_key():
    if len(sys.argv) > 1 and sys.argv[1].startswith("Bearer"):
        return sys.argv[1]
    return "Bearer TU_API_KEY_AQUI"

def log_message(message_type, content):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message_type}: {content}\n"
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_entry)

def generate_response(prompt, api_key):
    payload = {
        "prompt": prompt,
        "max_tokens": 2048,
        "temperature": 0.7,
        "top_p": 0.95,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": api_key,
    }

    try:
        response = requests.post(API_URL, headers=headers, data=json.dumps(payload), timeout=30)
        response.raise_for_status()
        return response.json()["text"].strip()
    except requests.exceptions.Timeout:
        log_message("Error", "Tiempo de espera agotado")
        return "Error: Tiempo de espera agotado al conectar con el servicio."
    except requests.exceptions.RequestException as e:
        log_message("Error", str(e))
        return f"Error de conexión: {str(e)}"
    except Exception as e:
        log_message("Error", str(e))
        return f"Error inesperado: {str(e)}"

def main():
    if len(sys.argv) < 2:
        user_input = "Hola, ¿en qué puedo ayudarte?"
    else:
        user_input = ' '.join(sys.argv[1:])

    print("Agente de chat iniciado. Consulta:", user_input, "\n")
    log_message("Solicitud", user_input)

    api_key = get_api_key()
    full_prompt = DEFAULT_PROMPT + user_input
    response_text = generate_response(full_prompt, api_key)

    print("Respuesta del agente:\n", response_text, "\n")
    log_message("Respuesta", response_text)

    # Resumen ejecutivo
    print("Resumen ejecutivo:")
    print("- Consulta procesada:", len(user_input.split()) if user_input else 0, "palabras")
    print("- Respuesta generada:", len(response_text.split()) if response_text else 0, "palabras")
    print("- Tiempo de procesamiento:", "Aproximado (no medido en esta versión)")
    print("- Estado:", "Completado" if response_text else "Fallido")

if __name__ == "__main__":
    main()