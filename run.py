#!/usr/bin/env python3
import requests
import socket
import os
import json
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

MAX_MESSAGES = 20
SUMMARY_FILE = "memory.json"

if os.path.exists(SUMMARY_FILE):
    with open(SUMMARY_FILE, "r") as f:
        summary_memory = f.read().strip()
else:
    summary_memory = ""

history = [{"role": "system", "content": SYSTEM_PROMPT}]

if summary_memory:
    history.append({"role": "system", "content": f"Conversation summary so far: {summary_memory}"})

def groq_call(messages):
    payload = {
        "model": MODEL,
        "messages": messages
    }
    r = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]

def summarize():
    global history, summary_memory
    convo = "\n".join([f"{m['role']}: {m['content']}" for m in history if m["role"] != "system"])
    prompt = [
        {"role": "system", "content": "Summarize this conversation in Spanish preserving important technical facts."},
        {"role": "user", "content": convo}
    ]
    summary = groq_call(prompt)
    summary_memory = summary
    with open(SUMMARY_FILE, "w") as f:
        f.write(summary)
    history = [{"role": "system", "content": SYSTEM_PROMPT}]
    history.append({"role": "system", "content": f"Conversation summary so far: {summary_memory}"})

def ask(question):
    global history
    history.append({"role": "user", "content": question})
    answer = groq_call(history)
    history.append({"role": "assistant", "content": answer})
    if len(history) > MAX_MESSAGES:
        summarize()
    return answer

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
