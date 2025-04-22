import json, os

def salvar_memoria(dados):
    with open("memory/memoria.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)

def carregar_memoria():
    if not os.path.exists("memory/memoria.json"):
        return {"historico": [], "preferencias": {}, "tarefas": []}
    with open("memory/memoria.json", "r", encoding="utf-8") as f:
        return json.load(f)