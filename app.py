from flask import Flask, request, jsonify
from config import openai_api_key, webhook_make
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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
