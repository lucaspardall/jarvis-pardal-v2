from flask import Flask, request, render_template_string
from agent import conversar_jarvis
from tools.speaker import falar

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>JARVIS.PARDAL</title>
</head>
<body style="font-family:Arial; padding:20px;">
  <h2>JARVIS.PARDAL v2.0</h2>
  <form method="post">
    <label>Você:</label><br>
    <input name="prompt" style="width:500px" autofocus><br><br>
    <input type="submit" value="Enviar">
  </form>
  {% if resposta %}
    <p><b>Jarvis:</b> {{ resposta }}</p>
  {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def home():
    resposta = ""
    if request.method == "POST":
        prompt = request.form["prompt"]
        resposta = conversar_jarvis(prompt)
        falar(resposta)
    return render_template_string(HTML, resposta=resposta)

if __name__ == "__main__":
    app.run(debug=True, port=5000)