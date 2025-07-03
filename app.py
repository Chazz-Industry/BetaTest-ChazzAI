from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PROMPT_FILE = os.getenv("PROMPT_FILE")

with open(PROMPT_FILE, "r", encoding="utf-8") as file:
    BASE_PROMPT = file.read()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    context = data.get("context", "").strip()
    mode = data.get("mode", "rewrite")

    prompt = BASE_PROMPT

    if context:
        prompt += f"\nContexte de la conversation : {context}\n"

    if mode == "rewrite":
        prompt += f'\nRéécris ce message dans un style Cocky & Funny comme le ferait Mystery : "{user_message}"'
    else:
        prompt += f"\nGénère une réponse fun, séduisante et calibrée dans ce contexte."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        suggestion = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Erreur API :", e)
        suggestion = "Erreur lors de la reformulation."

    return jsonify({"suggestion": suggestion})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
