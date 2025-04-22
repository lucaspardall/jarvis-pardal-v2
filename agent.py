import openai
import yaml
from tools.utils import carregar_memoria, salvar_memoria

with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

openai.api_key = config["openai_api_key"]
memoria = carregar_memoria()

def conversar_jarvis(prompt_usuario):
    memoria["historico"].append({"usuario": prompt_usuario})
    system_prompt = "Você é a JARVIS.PARDAL, braço direito do Imperador Lucas. Fale com formalidade, com tom britânico, e responda como um comandante digital."

    mensagens = [{"role": "system", "content": system_prompt}]
    for entrada in memoria["historico"][-10:]:
        mensagens.append({"role": "user", "content": entrada["usuario"]})

    resposta = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=mensagens
    )

    conteudo = resposta.choices[0].message.content.strip()
    memoria["historico"].append({"jarvis": conteudo})
    salvar_memoria(memoria)
    return conteudo