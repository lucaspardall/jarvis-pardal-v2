from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configuração GPT-4.1
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração Firebase
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

@app.route("/", methods=["GET"])
def index():
    return "JARVIS SUPREME ONLINE — GPT + Firebase + ElevenLabs + Make"

@app.route("/conversar", methods=["POST"])
def conversar():
    data = request.get_json()
    pergunta = data.get("mensagem")

    if not pergunta:
        return jsonify({"erro": "Mensagem não encontrada"}), 400

    # Consultar memória (exemplo básico)
    memoria_ref = db.collection('memoria').document('contexto')
    memoria_doc = memoria_ref.get()
    contexto = memoria_doc.to_dict() if memoria_doc.exists else {}

    # Chamar GPT-4.1 com contexto
    resposta_gpt = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Você é a Jarvis, assistente inteligente do comandante."},
            {"role": "user", "content": f"Contexto: {contexto}\nPergunta: {pergunta}"}
        ]
    )

    resposta_texto = resposta_gpt.choices[0].message.content.strip()

    # Salvar interação na memória
    db.collection('memoria').document('contexto').set({"ultima_interacao": pergunta})

    # Disparar Make se detectar ação (exemplo simples)
    if "executar" in resposta_texto.lower():
        requests.post(os.getenv("MAKE_WEBHOOK_URL"), json={"acao": resposta_texto})

    return jsonify({"resposta": resposta_texto})

@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    texto = data.get('mensagem')

    if not texto:
        return jsonify({"erro": "Texto não encontrado"}), 400

    headers = {
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY"),
        "Content-Type": "application/json"
    }

    body = {
        "text": texto,
        "voice_settings": { "stability": 0.5, "similarity_boost": 0.75 }
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
    else:
        return jsonify({"erro": "Erro ao gerar áudio"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
