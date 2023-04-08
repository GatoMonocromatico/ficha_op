from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return "pagina central"

@app.route("/<string:input>")
def ficha(input):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    requisicao_nome_personagem = requests.get(f"{bd}/personagens/{input}/.json")

    if requisicao_nome_personagem.text == 'null':
        return "error"
    else:
        return render_template("index.html", nome=input.capitalize())


if __name__ == "__main__":
    app.run(debug=True)
