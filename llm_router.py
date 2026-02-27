"""
ÁREA: CEREBRO
DESCRIPCIÓN: Motor de LLM con rotación automática de proveedores. Si uno falla o
llega al límite, pasa automáticamente al siguiente. Soporta Groq, Cerebras, Gemini,
Mistral, OpenRouter y LM Studio local. Importar en cualquier agente en lugar de
llamar a Groq directamente.
TECNOLOGÍA: Groq, Cerebras, Gemini, Mistral, OpenRouter, LM Studio
"""

import os
import sys
import time
import json
import requests
import io as _io
from datetime import datetime

# Fix Unicode para Windows (cp1252)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stdout, "buffer"):
    sys.stdout = open(sys.stdout.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
elif hasattr(sys.stderr, "buffer"):
    sys.stderr = open(sys.stderr.fileno(), mode="w", encoding="utf-8", errors="replace", closefd=False)

# Carga el .env automáticamente si existe
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # sin python-dotenv, usa variables de entorno del sistema

# ─────────────────────────────────────────────
#  CONFIGURACIÓN DE PROVEEDORES
#  Orden de prioridad: el primero disponible gana
# ─────────────────────────────────────────────

PROVEEDORES = [
    {
        "nombre": "Groq",
        "tipo": "groq",
        "api_key": os.environ.get("GROQ_API_KEY", ""),
        "modelo": "llama-3.3-70b-versatile",
        "activo": True,
    },
    {
        "nombre": "Cerebras",
        "tipo": "cerebras",
        "api_key": os.environ.get("CEREBRAS_API_KEY", ""),
        "modelo": "llama3.3-70b",
        "activo": True,
    },
    {
        "nombre": "Gemini",
        "tipo": "gemini",
        "api_key": os.environ.get("GEMINI_API_KEY", ""),
        "modelo": "gemini-2.0-flash",
        "activo": True,
    },
    {
        "nombre": "Mistral",
        "tipo": "mistral",
        "api_key": os.environ.get("MISTRAL_API_KEY", ""),
        "modelo": "mistral-small-latest",
        "activo": True,
    },
    {
        "nombre": "OpenRouter",
        "tipo": "openrouter",
        "api_key": os.environ.get("OPENROUTER_API_KEY", ""),
        "modelo": "meta-llama/llama-3.3-70b-instruct:free",
        "activo": True,
    },
    {
        "nombre": "LMStudio",
        "tipo": "lmstudio",
        "api_key": "local",
        "modelo": "local-model",
        "activo": True,
    },
]

# ─────────────────────────────────────────────
#  LLAMADAS POR PROVEEDOR
# ─────────────────────────────────────────────

def _llamar_groq(proveedor, messages, temperatura, max_tokens):
    from groq import Groq
    client = Groq(api_key=proveedor["api_key"])
    resp = client.chat.completions.create(
        model=proveedor["modelo"],
        messages=messages,
        temperature=temperatura,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _llamar_cerebras(proveedor, messages, temperatura, max_tokens):
    from cerebras.cloud.sdk import Cerebras
    client = Cerebras(api_key=proveedor["api_key"])
    resp = client.chat.completions.create(
        model=proveedor["modelo"],
        messages=messages,
        temperature=temperatura,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _llamar_gemini(proveedor, messages, temperatura, max_tokens):
    from google import genai
    client = genai.Client(api_key=proveedor["api_key"])
    # Convierte formato messages a texto para Gemini
    texto = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in messages])
    resp = client.models.generate_content(
        model=proveedor["modelo"],
        contents=texto,
    )
    return resp.text.strip()


def _llamar_mistral(proveedor, messages, temperatura, max_tokens):
    from mistralai import Mistral
    client = Mistral(api_key=proveedor["api_key"])
    resp = client.chat.complete(
        model=proveedor["modelo"],
        messages=messages,
        temperature=temperatura,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _llamar_openrouter(proveedor, messages, temperatura, max_tokens):
    resp = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {proveedor['api_key']}",
            "Content-Type": "application/json",
        },
        json={
            "model": proveedor["modelo"],
            "messages": messages,
            "temperature": temperatura,
            "max_tokens": max_tokens,
        },
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


def _llamar_lmstudio(proveedor, messages, temperatura, max_tokens):
    resp = requests.post(
        "http://localhost:1234/v1/chat/completions",
        headers={"Content-Type": "application/json"},
        json={
            "messages": messages,
            "temperature": temperatura,
            "max_tokens": max_tokens,
        },
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"].strip()


# ─────────────────────────────────────────────
#  MOTOR PRINCIPAL CON ROTACIÓN
# ─────────────────────────────────────────────

def _log(mensaje):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("registro_noche.txt", "a", encoding="utf-8") as f:
        f.write(f"[{ts}] [LLM_ROUTER] {mensaje}\n")


def completar(
    messages,
    temperatura=0.5,
    max_tokens=1000,
    proveedor_preferido=None,
    verbose=False,
):
    """
    Llama al LLM con rotación automática de proveedores.

    Args:
        messages: Lista de dicts {"role": "user/system/assistant", "content": "..."}
        temperatura: 0.0-1.0
        max_tokens: Máximo de tokens en la respuesta
        proveedor_preferido: Nombre del proveedor a intentar primero (opcional)
        verbose: Si True, imprime qué proveedor se usó

    Returns:
        String con la respuesta del LLM
    """
    LLAMADORES = {
        "groq":       _llamar_groq,
        "cerebras":   _llamar_cerebras,
        "gemini":     _llamar_gemini,
        "mistral":    _llamar_mistral,
        "openrouter": _llamar_openrouter,
        "lmstudio":   _llamar_lmstudio,
    }

    # Reordena si hay preferido
    proveedores = PROVEEDORES.copy()
    if proveedor_preferido:
        proveedores = sorted(
            proveedores,
            key=lambda p: 0 if p["nombre"].lower() == proveedor_preferido.lower() else 1
        )

    errores = []

    for proveedor in proveedores:
        if not proveedor["activo"]:
            continue

        # Salta si no tiene key configurada (excepto LMStudio que es local)
        if proveedor["tipo"] != "lmstudio" and not proveedor["api_key"]:
            continue

        tipo = proveedor["tipo"]
        llamador = LLAMADORES.get(tipo)
        if not llamador:
            continue

        try:
            if verbose:
                print(f"  [LLM] Usando {proveedor['nombre']}...")

            resultado = llamador(proveedor, messages, temperatura, max_tokens)

            _log(f"OK → {proveedor['nombre']} | tokens_aprox:{len(resultado.split())}")
            return resultado

        except Exception as e:
            error_str = str(e).lower()
            error_msg = f"{proveedor['nombre']}: {str(e)[:120]}"
            errores.append(error_msg)

            if "rate_limit" in error_str or "429" in error_str:
                _log(f"Rate limit en {proveedor['nombre']} — rotando al siguiente")
            elif "invalid" in error_str and "key" in error_str:
                _log(f"Key inválida en {proveedor['nombre']} — rotando al siguiente")
            else:
                _log(f"Error en {proveedor['nombre']}: {str(e)[:100]} — rotando")

            time.sleep(1)
            continue

    # Todos fallaron
    _log(f"TODOS los proveedores fallaron: {' | '.join(errores)}")
    return None


def completar_simple(prompt, sistema=None, temperatura=0.5, max_tokens=1000):
    """
    Versión simplificada para uso rápido con un solo prompt.

    Args:
        prompt: El mensaje del usuario
        sistema: Instrucción de sistema opcional
        temperatura: 0.0-1.0
        max_tokens: Máximo tokens respuesta

    Returns:
        String con la respuesta
    """
    messages = []
    if sistema:
        messages.append({"role": "system", "content": sistema})
    messages.append({"role": "user", "content": prompt})
    return completar(messages, temperatura=temperatura, max_tokens=max_tokens)


def ver_estado():
    """Muestra qué proveedores están configurados y disponibles."""
    print("\n📡 ESTADO DE PROVEEDORES LLM")
    print("─" * 40)
    for p in PROVEEDORES:
        if p["tipo"] == "lmstudio":
            estado = "🟡 Local (necesita LM Studio corriendo)"
        elif p["api_key"]:
            estado = "🟢 Configurado"
        else:
            estado = "🔴 Sin API key (.env)"
        print(f"  {p['nombre']:12} {estado}")
        print(f"  {'':12} Modelo: {p['modelo']}")
    print("─" * 40)
    configurados = sum(1 for p in PROVEEDORES if p["api_key"] or p["tipo"] == "lmstudio")
    print(f"  Disponibles: {configurados}/{len(PROVEEDORES)}\n")


# ─────────────────────────────────────────────
#  CÓMO USAR EN TUS AGENTES
# ─────────────────────────────────────────────
# Antes (solo Groq):
#   from groq import Groq
#   client = Groq(api_key="...")
#   resp = client.chat.completions.create(...)
#
# Ahora (con rotación automática):
#   from llm_router import completar_simple, completar
#
#   # Versión simple:
#   resultado = completar_simple("¿Cuánto es el ISR de $50,000?")
#
#   # Versión con historial:
#   resultado = completar([
#       {"role": "system", "content": "Eres experto en finanzas mexicanas"},
#       {"role": "user", "content": "¿Cuánto es el ISR de $50,000?"}
#   ])
# ─────────────────────────────────────────────

if __name__ == "__main__":
    ver_estado()
    print("🧪 Probando rotación...")
    resultado = completar_simple(
        "Di exactamente: 'Router LLM funcionando correctamente'",
        max_tokens=20
    )
    if resultado:
        print(f"✅ Respuesta: {resultado}")
    else:
        print("❌ Todos los proveedores fallaron. Revisa tu .env")