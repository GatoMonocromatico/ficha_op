from flask import Flask, render_template, request, url_for, redirect
import requests

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        nome = request.form['input']

        if nome != "":
            bd = "https://op-database-728c3-default-rtdb.firebaseio.com/nomes"
            requisicao = requests.get(f"{bd}/.json")
            personagens = requisicao.json()

            if nome in personagens:
                return redirect(url_for('ficha', input=nome))

            else:
                return render_template("pagina_central.html", erro="Personagem não existe.")

    return render_template("pagina_central.html", erro="")

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
