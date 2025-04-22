from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuração GPT
openai.api_key = os.getenv("OPENAI_API_KEY")

# Firebase
firebase_json = os.getenv("FIREBASE_CONFIG")
if firebase_json:
    cred = credentials.Certificate(json.loads(firebase_json))
    firebase_admin.initialize_app(cred)
    db = firestore.client()
else:
    db = None  # Garante que não quebre o servidor se não estiver setado

# Serve HTML
@app.route("/", methods=["GET"])
def serve_index():
    return app.send_static_file("index.html")

# Rota de conversa
@app.route("/conversar", methods=["POST"])
def conversar():
    data = request.get_json()
    pergunta = data.get("mensagem")

    if not pergunta:
        return jsonify({"erro": "Mensagem não encontrada"}), 400

    contexto = {}
    if db:
        doc_ref = db.collection("memoria").document("contexto")
        doc = doc_ref.get()
        contexto = doc.to_dict() if doc.exists else {}

    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é a Jarvis, assistente inteligente e proativa do comandante."},
            {"role": "user", "content": f"Contexto atual: {contexto}\nPergunta: {pergunta}"}
        ]
    )

    resposta_texto = resposta.choices[0].message.content.strip()

    if db:
        doc_ref.set({"ultima_interacao": pergunta})

    if "executar" in resposta_texto.lower():
        requests.post(os.getenv("MAKE_WEBHOOK_URL", ""), json={"acao": resposta_texto})

    return jsonify({"resposta": resposta_texto})

# Voz
@app.route("/speak", methods=["POST"])
def speak():
    data = request.get_json()
    texto = data.get("mensagem")

    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }

    body = {
        "text": texto,
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}",
        json=body,
        headers=headers
    )

    if response.status_code == 200:
        with open("voz_jarvis.mp3", "wb") as f:
            f.write(response.content)
        return send_file("voz_jarvis.mp3", mimetype="audio/mpeg")

    return jsonify({"erro": "Erro ao gerar áudio"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
