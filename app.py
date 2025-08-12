from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import requests
import tempfile

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
PROMPT_FILE = os.getenv("PROMPT_FILE")

with open(PROMPT_FILE, "r", encoding="utf-8") as file:
    BASE_PROMPT = file.read()

app = Flask(__name__)

def build_prompt(user_message: str, context: str = "", prompt_type: str = "rewrite") -> str:
    prompt = BASE_PROMPT
    if context:
        prompt += f"\nContexte : {context}\n"

    if prompt_type == "rewrite":
        prompt += f'\nRéécris ce message dans un style détendu, léger et fun : "{user_message}"'
    elif prompt_type == "generate":
        if user_message == "":
            prompt += f"\nGénère un contenu adapté au contexte : '{context}'"
        else:
            prompt += f'\nGénère une réponse fun et calibrée à ce message dans le contexte : "{user_message}"'
    return prompt

def generate_response(prompt: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        suggestion = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"suggestion": suggestion}
    except Exception as e:
        print(f"Erreur API : {e}")
        return {"error": "Erreur lors de la génération."}

@app.route("/")
def home():
    ga_id = os.getenv("GA_ID")
    return render_template("index.html", ga_id=ga_id)

@app.route("/rewrite", methods=["POST"])
def rewrite():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    context = data.get("context", "").strip()

    if not user_message:
        return jsonify({"error": "Le message est vide."}), 400

    prompt = build_prompt(user_message, context, "rewrite")
    result = generate_response(prompt)
    return jsonify(result)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    context = data.get("context", "").strip()

    prompt = build_prompt(user_message, context, "generate")
    result = generate_response(prompt)
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))