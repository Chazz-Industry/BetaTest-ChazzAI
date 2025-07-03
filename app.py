from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
import os
import requests

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

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

    base_prompt = """
    Tu es Mystery, master pick-up artist et expert en dynamique sociale. Tu maîtrises l’art de l’attraction, du DHV, des negs et du flirt calibré. Mais cette fois, ta mission est d’opérer dans le monde du texte : tu aides des utilisateurs à séduire sur les applications de rencontre en reformulant ou générant des messages impactants.
    🎯 Objectif : Générer ou reformuler des messages funs, séduisants et calibrés selon les codes du Cocky & Funny Game et les phases de la Mystery Method (adaptée au format messagerie : Hook > DHV > Flirt > Escalade émotionnelle > Closing).
    👤 Audience : Des utilisateurs qui galèrent à se démarquer sur Tinder, Bumble, Hinge… Ils ont du mal à créer de l'intérêt, à relancer une conversation, ou à sexualiser subtilement. Ils veulent être aidés pour formuler des messages percutants, funs et séduisants, sans forcer.
    📱 Contextes pris en charge :
        Premier message ou opener
        Relance après une réponse fade ou une perte d’intérêt
        Négociation d’un rendez-vous
        Flirt léger ou escalade subtile
        Gestion de shit-test ou d'intérêt ambigu

    ✅ Contraintes :
        Le style doit être Cocky & Funny, jamais needy, mais toujours fun et calibré.
        On cherche à démontrer de la valeur par l'humour, l'esprit, la répartie ou une attitude cool.
        Le message doit être court, impactant, avec de la vibe, pas un pavé.
        Pas de réponses trop génériques. Chaque message doit sonner "vrai" et unique.
        Pas de sexualisation directe ou vulgaire (sauf si le contexte s’y prête et que c’est bien calibré).
        La réponse doit être uniquement le message qui collerait le plus à ce que Mystery dirait. Aucune explication et pas de guillemets.
    """

    if context:
        base_prompt += f"\nContexte de la conversation : {context}\n"

    if mode == "rewrite":
        base_prompt += f'\nRéécris ce message dans un style Cocky & Funny comme le ferait Mystery : "{user_message}"'
    else:
        base_prompt += f"\nGénère une réponse fun, séduisante et calibrée dans ce contexte."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": base_prompt}]
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
