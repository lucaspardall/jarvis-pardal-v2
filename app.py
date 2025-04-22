from flask import Flask, request, jsonify
from config import openai_api_key, webhook_make

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