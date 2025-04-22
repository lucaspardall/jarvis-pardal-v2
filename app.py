from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/")
def home():
    return "JARVIS ONLINE"

@app.route("/conversar", methods=["POST"])
def conversar_jarvis():
    dados = request.json
    mensagem_usuario = dados.get("mensagem", "")

    if not mensagem_usuario:
        return jsonify({"erro": "Mensagem não fornecida"}), 400

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": mensagem_usuario}]
        )
        return jsonify({"resposta": resposta.choices[0].message.content})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
