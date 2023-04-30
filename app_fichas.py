import json
from flask import Flask, render_template, request, url_for, redirect
import requests
import re
from manipulador_personagens import Personagem
# import time

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        nome = request.form['input']

        if nome != "":
            bd = "https://op-database-728c3-default-rtdb.firebaseio.com/nomes"
            requisicao = requests.get(f"{bd}/.json")
            personagens = requisicao.json()

            padrao = re.compile(r"[a-z]")

            nome_formatado = nome.lower()

            for letra in nome:
                if not padrao.search(letra):
                    nome_formatado = nome_formatado.replace(letra, "")

            if nome_formatado in personagens:
                return redirect(url_for('ficha', input=nome_formatado))

            else:
                return render_template("pagina_central.html", erro=f'Personagem "{nome}" não existe.')

    return render_template("pagina_central.html", erro="")


@app.route("/<string:input>")
def ficha(input):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    requisicao_nome_personagem = requests.get(f"{bd}/personagens/{input}/.json")

    if requisicao_nome_personagem.text == 'null':
        return "error"
    else:
        return render_template("index.html", nome=input.capitalize())


@app.route("/*-*-controlexp", methods=["POST", "GET"])
def controle_xp():
    if request.method == "POST":
        bd = "https://op-database-728c3-default-rtdb.firebaseio.com"
        vd = request.form['vd']

        lista_nomes = []
        for item in request.form:
            if item != "vd" and item != "repetir":
                lista_nomes.append(item.replace("_", " "))

        if lista_nomes:
            for nome in lista_nomes:
                requisicao_xp_atual = requests.get(f"{bd}/personagens/{nome}/xp/.json").json()
                requisicao_ultima_mudanca_xp = requests.get(f"{bd}/personagens/{nome}/ultimo_xp_ganho/.json").json()
                if type(requisicao_ultima_mudanca_xp) != int:
                    requisicao_ultima_mudanca_xp_int = requisicao_ultima_mudanca_xp.split(" ")[0]
                else:
                    requisicao_ultima_mudanca_xp_int = requisicao_ultima_mudanca_xp

                xp_ganhar = round(int(vd)**2.2787536)

                if xp_ganhar == requisicao_ultima_mudanca_xp_int and "repetir" not in request.form:
                    continue
                elif "repetir" in request.form and "repetido" in str(requisicao_ultima_mudanca_xp):
                    continue

                dados = {
                    "xp": xp_ganhar + requisicao_xp_atual,
                    "ultimo_xp_ganho": xp_ganhar if xp_ganhar != requisicao_ultima_mudanca_xp_int else f"{xp_ganhar} repetido"
                }

                requests.patch(f"{bd}/personagens/{nome}/.json", data=json.dumps(dados))

            requisicao_nomes = requests.get(f"{bd}/nomes/.json")
            nomes = [nome for nome in requisicao_nomes.json()]

            for nome in nomes:
                personagem = Personagem(nome)

                if personagem.verifica_upou_de_nivel():
                    upar = {f"{nome}": True}
                    requests.patch(f"{bd}/nomes/.json", data=json.dumps(upar))
                else:
                    upar = {f"{nome}": False}
                requests.patch(f"{bd}/nomes/.json", data=json.dumps(upar))

            return render_template("controle_xp.html", status="Ok!")
        else:
            return render_template("controle_xp.html", status="ERRO - Não selecionou nenhum personagem!")

    if not request.form:
        return render_template("controle_xp.html", status="Ok!")


if __name__ == "__main__":
    app.run(debug=True)
