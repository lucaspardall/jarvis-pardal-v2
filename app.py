from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import requests
import openai
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

app = Flask(__name__, static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# Configuração GPT-4.1
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configuração Firebase via variável de ambiente
firebase_json = os.getenv("FIREBASE_CONFIG")
cred = credentials.Certificate(json.loads(firebase_json))
firebase_admin.initialize_app(cred)
db = firestore.client()

# Serve o Painel
@app.route("/", methods=["GET"])
def serve_index():
    return app.send_static_file('index.html')

@app.route("/conversar", methods=["POST"])
def conversar():
    data = request.get_json_
