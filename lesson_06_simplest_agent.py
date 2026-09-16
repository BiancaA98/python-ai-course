import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI


def main():
    # Incarca variabilele din fisierul .env
    load_dotenv(Path(__file__).resolve().with_name(".env"))

    # Conectare la OpenRouter
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER_API_KEY")
    )

    # Lista de mesaje
    messages = []

    # System prompt
    messages.append({
        "role": "system",
        "content": "Use run_tests tool when asked to run any tests."
    })

    # Mesajul utilizatorului
    messages.append({
        "role": "user",
        "content": input("you> ")
    })

    # Tools disponibile pentru agent
    tools = [
        {
            "type": "function",
            "function": {
                "name": "run_tests",
                "description": "Run uv run pytest."
            }
        }
    ]

    # Trimite cererea catre model
    response = client.chat.completions.create(
        messages=messages,
        model=os.getenv("OPEN_ROUTER_MODEL_NAME"),
        tools=tools
    ).choices[0].message

    # Afiseaza raspunsul
    print(response)


if __name__ == "__main__":
    main()
