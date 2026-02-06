import ollama

MODEL = "llama3:8b"  # luego puedes cambiar a "gpt-oss:20b"

def main():
    print("Agente local listo. Escribe 'salir' para terminar.\n")
    while True:
        user = input("Tú: ").strip()
        if user.lower() in ("salir", "exit", "quit"):
            break

        resp = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": "Eres un asistente útil, directo y práctico."},
                {"role": "user", "content": user},
            ],
        )
        print("\nAgente:", resp["message"]["content"].strip(), "\n")

if __name__ == "__main__":
    main()
