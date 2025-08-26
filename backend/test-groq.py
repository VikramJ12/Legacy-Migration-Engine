import os
import requests

# Set your API key here or ensure it's in your environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY')
GROQ_CHAT_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "llama3-70b-8192"  # You can change this to another Groq-supported model

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY environment variable not set.")

headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

data = {
    "model": GROQ_MODEL,
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write a Python function that returns the factorial of a number."}
    ],
    "max_tokens": 256,
    "temperature": 0.2
}

response = requests.post(GROQ_CHAT_URL, headers=headers, json=data, timeout=60)
print("Status code:", response.status_code)
print("Response:")
print(response.json())