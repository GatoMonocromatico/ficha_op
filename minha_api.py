from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)


@app.route('/alterar/pte', methods=["GET", "POST"])
def ficha():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    acao = informacoes["ação"]
    pte_mod = {"pv": str(informacoes["pv"]).replace("-", ""),
               "pe": str(informacoes["pe"]).replace("-", ""),
               "sn": str(informacoes["sn"]).replace("-", "")}

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    requisicao_pegar_pte = requests.get(f"{bd}/.json")
    todas_informacoes = requisicao_pegar_pte.json()

    dict_pte = {"pv": {"maximo": int(todas_informacoes["pv"]["maximo"]), "atual": int(todas_informacoes["pv"]["atual"])},
                "pe": {"maximo": int(todas_informacoes["pe"]["maximo"]), "atual": int(todas_informacoes["pe"]["atual"])},
                "sn": {"maximo": int(todas_informacoes["sn"]["maximo"]), "atual": int(todas_informacoes["sn"]["atual"])}}

    for est in pte_mod:
        valor_est = pte_mod[est]

        try:
            valor_est = int(valor_est)

            if acao == "dano":
                if valor_est > dict_pte[est]['atual']:
                    valor_est = int(dict_pte[est]['atual'])

                pte_mod[est] = valor_est * -1

            else:
                if valor_est > dict_pte[est]['maximo'] - dict_pte[est]['atual']:
                    valor_est = dict_pte[est]['maximo'] - dict_pte[est]['atual']

                pte_mod[est] = int(valor_est)

        except ValueError:
            valor_est = 0
            pte_mod[est] = valor_est

    pv_final = dict_pte['pv']['atual'] + pte_mod["pv"]
    pe_final = dict_pte['pe']['atual'] + pte_mod["pe"]
    sn_final = dict_pte['sn']['atual'] + pte_mod["sn"]

    dict_pte['pv']['atual'] = pv_final
    dict_pte['pe']['atual'] = pe_final
    dict_pte['sn']['atual'] = sn_final

    dict_len_maximo_pte = {"maximo": 0, "atual": 0}

    for pte in dict_pte:
        for tipo in dict_pte[pte]:
            numero = dict_pte[pte][tipo]

            if len(str(numero)) > dict_len_maximo_pte[tipo]:
                dict_len_maximo_pte[tipo] = len(str(numero))

    for pte in dict_pte:
        for tipo in dict_pte[pte]:
            while len(str(dict_pte[pte][tipo])) < dict_len_maximo_pte[tipo]:
                dict_pte[pte][tipo] = f"0{dict_pte[pte][tipo]}"

            dict_pte[pte][tipo] = str(dict_pte[pte][tipo])

    pv_formatado = f"PV: {dict_pte['pv']['atual']}/{dict_pte['pv']['maximo']}"
    pe_formatado = f"PE: {dict_pte['pe']['atual']}/{dict_pte['pe']['maximo']}"
    sn_formatado = f"SN: {dict_pte['sn']['atual']}/{dict_pte['sn']['maximo']}"

    dados_return = {"pv": pv_formatado,
                    "pe": pe_formatado,
                    "sn": sn_formatado}

    dados = {"pv": {"atual": pv_final, "maximo": int(todas_informacoes["pv"]["maximo"])},
             "pe": {"atual": pe_final, "maximo": int(todas_informacoes["pe"]["maximo"])},
             "sn": {"atual": sn_final, "maximo": int(todas_informacoes["sn"]["maximo"])}}

    requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return jsonify(dados_return)


@app.route("/receber-formatado/<string:personagem>", methods=["GET"])
def retorna_dados_formatado(personagem):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    requisita_dados_personagem = requests.get(f"{bd}/personagens/{personagem}/.json")
    dados_personagem = requisita_dados_personagem.json()

    anotacoes = dados_personagem["anotações"]
    atributos = dados_personagem["atributos"]
    defesa = dados_personagem["defesa"]
    inventario = dados_personagem["inventario"]
    nex = f"{dados_personagem['nex']}%"
    pericias = dados_personagem["pericias"]
    poderes = dados_personagem["poderes"]
    rituais = dados_personagem["rituais"]
    classe = dados_personagem["classe"]
    trilha = dados_personagem["trilha"]
    origem = dados_personagem["origem"]
    afinidade = dados_personagem["afinidade"]

    infos = f"Afinidade:\n{afinidade}\n\nClasse:\n{classe}\n\nOrigem:\n{origem}\n\nTrilha:\n{trilha}"

    dict_pte = {"pe": dados_personagem["pe"],
                "pv": dados_personagem["pv"],
                "sn": dados_personagem["sn"]}

    if len(nex) == 2:
        nex = f"0{nex}"

    nex = f"Nex: {nex}"

    dict_len_maximo_pte = {"maximo": 0, "atual": 0}

    for pte in dict_pte:
        for tipo in dict_pte[pte]:
            numero = int(dict_pte[pte][tipo])

            if len(str(numero)) > dict_len_maximo_pte[tipo]:
                dict_len_maximo_pte[tipo] = len(str(numero))

    for pte in dict_pte:
        for tipo in dict_pte[pte]:
            dict_pte[pte][tipo] = int(dict_pte[pte][tipo])

            while len(str(dict_pte[pte][tipo])) < dict_len_maximo_pte[tipo]:
                dict_pte[pte][tipo] = f"0{dict_pte[pte][tipo]}"

    for pericia in pericias:
        nivel_treinamento = pericias[pericia]

        if nivel_treinamento == "nt":
            nivel_treinamento = "+0"
        elif nivel_treinamento == "t":
            nivel_treinamento = "+5"
        elif nivel_treinamento == "v":
            nivel_treinamento = "+10"
        else:
            nivel_treinamento = "+15"

        pericias[pericia] = nivel_treinamento

    if rituais != "":
        for ritual in rituais:
            circulo = f"{rituais[ritual][0]}º círculo"

            rituais[ritual] = f"({circulo})\n\n"
    else:
        rituais = "Nenhum"

    for poder in poderes:
        custo = poderes[poder][0]

        if custo == "0":
            custo = "(condição/passivo)"
        else:
            custo += "PE"

        poderes[poder] = custo

    for item in inventario:
        info = inventario[item]
        carga = info[:info.find(" ")]
        categoria = info.replace(f"{carga} ", "")

        inventario[item] = f"(Carga: {carga}|Categoria: {categoria})"

    inventario_formatado = ""
    for item in inventario:
        inventario_formatado += f"{item.capitalize()}\n{inventario[item]}\n\n"

    pericias_formatado = ""
    for pericia in pericias:
        pericias_formatado += f"{pericia.capitalize()} {pericias[pericia]}\n"

    for poder in poderes:
        poderes[poder] = f"{poder.capitalize()}\n{poderes[poder]}"

    if rituais != "Nenhum":
        for ritual in rituais:
            rituais[ritual] = f"{ritual.capitalize()}\n{rituais[ritual]}"

    pv_formatado = f"PV: {dict_pte['pv']['atual']}/{dict_pte['pv']['maximo']}"
    pe_formatado = f"PE: {dict_pte['pe']['atual']}/{dict_pte['pe']['maximo']}"
    sn_formatado = f"SN: {dict_pte['sn']['atual']}/{dict_pte['sn']['maximo']}"

    retorno = {"pv": pv_formatado,
               "pe": pe_formatado,
               "sn": sn_formatado,
               "anotações": anotacoes,
               "atributos": atributos,
               "infos": infos,
               "defesa": f"Defesa: {defesa}",
               "inventario": inventario_formatado,
               "nex": nex,
               "pericias": pericias_formatado,
               "poderes": poderes,
               "rituais": rituais}

    return jsonify(retorno)


@app.route("/receber/<string:personagem>", methods=["GET"])
def retorna_dados(personagem):
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    requisita_dados_personagem = requests.get(f"{bd}/personagens/{personagem}/.json")
    dados_personagem = requisita_dados_personagem.json()

    return jsonify(dados_personagem)

@app.route("/receber/pericias", methods=["POST"])
def retorna_pericias():
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    personagem = request.get_json()
    personagem = personagem["personagem"]

    requisita_pericias = requests.get(f"{bd}/personagens/{personagem}/pericias/.json")
    dados_personagem = requisita_pericias.json()

    return jsonify(dados_personagem)

@app.route("/receber/info", methods=["GET", "POST"])
def retorna_info():
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    informacoes = request.get_json()
    tipo = informacoes["tipo"]
    habilidade = informacoes["habilidade"].replace("_", " ").lower()

    requisita_info = requests.get(f"{bd}/info/{tipo}/{habilidade}/.json")
    info = requisita_info.json()

    if tipo == "rituais":
        iterador = 2
    else:
        iterador = 1

    return jsonify(info[iterador])


@app.route("/alterar/anotacoes", methods=["POST"])
def salva_anotacoes():
    informacoes = request.get_json()
    personagem = informacoes["personagem"]
    anotacoes = informacoes["anotações"]

    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/"

    dados = {"anotações": anotacoes}
    requisicao = requests.patch(f"{bd}/personagens/{personagem}/.json", data=json.dumps(dados))

    return jsonify(requisicao.json())


@app.route("/alterar/atributos", methods=["POST"])
def altera_atributos():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    agilidade = informacoes["agi"]
    forca = informacoes["for"]
    intelecto = informacoes["int"]
    presenca = informacoes["pre"]
    vigor = informacoes["vig"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}/atributos"

    dados = {"agi": agilidade, "for": forca, "int": intelecto, "pre": presenca, "vig": vigor,}

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/classe", methods=["POST"])
def altera_classe():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    classe = informacoes["classe"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"classe": classe}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/defesa", methods=["POST"])
def altera_defesa():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    defesa = informacoes["defesa"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"defesa": defesa}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/inventario", methods=["POST"])
def altera_inventario():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    inventario = informacoes["inventario"]
    dados = {"inventario": inventario}

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    requisicao_inventario_anterior = requests.get(f"{bd}/inventario/.json")
    inventario_anterior = requisicao_inventario_anterior.json()

    for item in inventario_anterior:
        if item not in dados["inventario"]:
            dados["inventario"][item] = inventario_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/nex", methods=["POST"])
def altera_nex():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    nex = informacoes["nex"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"nex": nex}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/origem", methods=["POST"])
def altera_origem():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    origem = informacoes["origem"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"origem": origem}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/pericias", methods=["POST"])
def altera_pericias():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    pericias = informacoes["pericias"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"pericias": pericias}

    requisicao_pericias_anterior = requests.get(f"{bd}/pericias/.json")
    pericias_anterior = requisicao_pericias_anterior.json()

    for item in pericias_anterior:
        if item not in dados["pericias"]:
            dados["pericias"][item] = pericias_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/poderes", methods=["POST"])
def altera_poderes():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    poderes = informacoes["poderes"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"poderes": poderes}

    requisicao_poderes_anterior = requests.get(f"{bd}/poderes/.json")
    poderes_anterior = requisicao_poderes_anterior.json()

    for item in poderes_anterior:
        if item not in dados["poderes"]:
            dados["poderes"][item] = poderes_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/rituais", methods=["POST"])
def altera_rituais():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    rituais = informacoes["rituais"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"rituais": rituais}

    requisicao_rituais_anterior = requests.get(f"{bd}/rituais/.json")
    rituais_anterior = requisicao_rituais_anterior.json()

    for item in rituais_anterior:
        if item not in dados["rituais"]:
            dados["rituais"][item] = rituais_anterior[item]

    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/alterar/trilha", methods=["POST"])
def altera_trilha():
    informacoes = request.get_json()

    personagem = informacoes["personagem"]
    trilha = informacoes["trilha"]

    bd = f"https://op-database-728c3-default-rtdb.firebaseio.com/personagens/{personagem}"

    dados = {"trilha": trilha}
    requisicao = requests.patch(f"{bd}/.json", data=json.dumps(dados))

    return requisicao.text


@app.route("/receber/nomes")
def retorna_nomes():
    bd = "https://op-database-728c3-default-rtdb.firebaseio.com/nomes"

    reuisicao = requests.get(f"{bd}/.json")
    nomes = reuisicao.json()

    return jsonify(nomes)


@app.after_request
def add_headers(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    # response.headers.add("Access-Control-Allow-Methods", "POST, GET")
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')

    return response


if __name__ == "__main__":
    app.run()
