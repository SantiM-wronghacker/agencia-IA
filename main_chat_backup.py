"""
ÁREA: HERRAMIENTAS
DESCRIPCIÓN: Agente de chat que utiliza la API de Groq para generar respuestas a preguntas del usuario
TECNOLOGÍA: Python, requests, json, Groq API
"""
import requests
import json
import sys
import time

MODEL = "llama-3.3-70b-versatile"
API_URL = "https://api.groq.com/v1/models/" + MODEL + "/generate"

def main():
    if len(sys.argv) < 2:
        user = "Hola, ¿en qué puedo ayudarte?"
    else:
        user = ' '.join(sys.argv[1:])

    print("Agente local listo. Parámetros: ", user, "\n")

    try:
        payload = {
            "prompt": "Eres un asistente útil, directo y práctico.\nTú: " + user,
            "max_tokens": 2048,
            "temperature": 0.7,
            "top_p": 0.95,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer TU_API_KEY_AQUI",  
        }

        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write("Solicitud: " + user + "\n")

        response = requests.post(API_URL, headers=headers, data=json.dumps(payload))

        if response.status_code == 200:
            resp = response.json()
            print("Agente:", resp["text"].strip(), "\n")
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write("Respuesta: " + resp["text"].strip() + "\n")
        else:
            print("Error:", response.status_code, "\n")
            with open('log.txt', 'a', encoding='utf-8') as f:
                f.write("Error: " + str(response.status_code) + "\n")
    except requests.exceptions.RequestException as e:
        print("Error de conexión:", e, "\n")
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write("Error de conexión: " + str(e) + "\n")
    except Exception as e:
        print("Error desconocido:", e, "\n")
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write("Error desconocido: " + str(e) + "\n")

    time.sleep(2)

if __name__ == "__main__":
    main()