#!/usr/bin/env python3
import requests
import socket
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
if not API_KEY:
    print("API key not found. Set GROQ_API_KEY in .env")
    exit(1)

requests.packages.urllib3.util.connection.allowed_gai_family = lambda: socket.AF_INET

API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

SYSTEM_PROMPT = (
    "You are a specialist in internetworking, microservices, operating systems, "
    "Docker, Bootstrap, PHP, MySQL, and application and network cybersecurity. "
    "Always answer in Spanish. Maximum 25 words."
)

def ask(question):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question}
        ]
    }
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def main():
    while True:
        q = input("[Jef]: ")
        if q.lower() in ["exit", "quit", "salir"]:
            break
        try:
            answer = ask(q)
            print(f"[Groq]: {answer}")
        except Exception as e:
            print("[Groq]: Error:", e)

if __name__ == "__main__":
    main()
