import os
import requests

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def send_to_llm(prompt: str):

    if not OPENAI_API_KEY:
        return {"error": "LLM API key missing"}

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        json=payload,
        headers=headers
    )

    return r.json()
