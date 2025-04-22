from flask import Flask, request, jsonify, send_file
import requests
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return "JARVIS está online!"

@app.route("/conversar", methods=["POST"])
def conversar():
    data = request.get_json()
    pergunta = data.get("mensagem")

    if not pergunta:
        return jsonify({"erro": "Mensagem não encontrada"}), 400

    return jsonify({"resposta": f"Você perguntou: {pergunta}"})

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

    VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # ID padrão, depois você pode customizar no ElevenLabs

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
