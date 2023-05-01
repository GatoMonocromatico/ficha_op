import requests
import json


class Personagem:
    def __init__(self, nome):
        self.nome = nome
        self.banco_dados = "https://op-database-728c3-default-rtdb.firebaseio.com"

        requisicao = requests.get(f"{self.banco_dados}/nomes/{self.nome}/.json").json()

        if requisicao is None:
            self.novo = True
        else:
            self.novo = False

        self.pericias_lista = ("acrobacia", "adestramento", "artes", "atletismo", "atualidades",
                               "ciências", "crime", "diplomacia", "enganação", "fortitude",
                               "furtividade", "iniciativa", "intimidação", "intuição", "investigação",
                               "luta", "medicina", "ocultismo", "percepção", "pilotagem",
                               "pontaria", "profissão", "reflexos", "religião", "sobrevivência",
                               "tática", "tecnologia", "vontade")

        if self.novo:
            self.nivel_de_exposicao = 0
            self.agilidade = 1
            self.forca = 1
            self.intelecto = 1
            self.presenca = 1
            self.vigor = 1
            self.atributos = {"agilidade": self.agilidade,
                              "força": self.forca,
                              "intelecto": self.intelecto,
                              "presença": self.presenca,
                              "vigor": self.vigor}
            self.limite_de_rituais_para_aprender = self.intelecto
            self.classe = ""
            self.vida = 0
            self.pontos_de_esforco = 0
            self.sanidade = 0
            self.poderes = []
            self.afinidade = "nenhuma"
            self.origem = ""
            self.pv_extra = 0
            self.pe_extra = 0
            self.sn_extra = 0
            self.pericias_treinadas = {}
            self.rituais = []
            self.trilha = ""
            self.numero_de_poderes_de_conhecimento_possuidos = 0
            self.numero_de_poderes_de_energia_possuidos = 0
            self.numero_de_poderes_de_morte_possuidos = 0
            self.numero_de_poderes_de_sangue_possuidos = 0
            self.circulo_ritual_maximo = 1
            self.nivel_de_treinamento_em_pericia_maximo = "treinado"
            self.xp = 0

            self.cria_e_melhora_atributos(4, True, False)
            self.atualiza_atributos()
            self.escolhe_origem()
            self.aumenta_nivel_de_exposicao()
        else:
            requisita_dados = requests.get(f"{self.banco_dados}/personagens/{self.nome}/.json")
            dados = requisita_dados.json()

            self.nivel_de_exposicao = dados["nex"]
            self.agilidade = dados["atributos"]["agi"]
            self.forca = dados["atributos"]["for"]
            self.intelecto = dados["atributos"]["int"]
            self.presenca = dados["atributos"]["pre"]
            self.vigor = dados["atributos"]["vig"]
            self.atributos = {"agilidade": self.agilidade,
                              "força": self.forca,
                              "intelecto": self.intelecto,
                              "presença": self.presenca,
                              "vigor": self.vigor}
            self.limite_de_rituais_para_aprender = dados["limite_rituais"]
            self.classe = dados["classe"]
            self.vida = dados["pv"]["maximo"]
            self.pontos_de_esforco = dados["pe"]["maximo"]
            self.sanidade = dados["sn"]["maximo"]
            self.afinidade = dados["afinidade"]
            self.origem = dados["origem"]

            self.pericias_treinadas = dados["pericias"]

            pericias_deletar = []
            for pericia in self.pericias_treinadas:
                if self.pericias_treinadas[pericia] == "nt":
                    pericias_deletar.append(pericia)
                elif self.pericias_treinadas[pericia] == "t":
                    self.pericias_treinadas[pericia] = "treinado"
                elif self.pericias_treinadas[pericia] == "v":
                    self.pericias_treinadas[pericia] = "veterano"
                elif self.pericias_treinadas[pericia] == "e":
                    self.pericias_treinadas[pericia] = "expert"

            for pericia in pericias_deletar:
                del self.pericias_treinadas[pericia]

            self.rituais = [ritual for ritual in dados["rituais"]]
            self.poderes = [poder for poder in dados["poderes"]]
            for ritual in self.rituais:
                self.poderes.append(f"{ritual} (círculo {dados['rituais'][ritual][0]})")

            self.trilha = dados["trilha"]

            self.numero_de_poderes_de_conhecimento_possuidos = dados["numero_de_poderes_de_conhecimento_possuidos"]
            self.numero_de_poderes_de_energia_possuidos = dados["numero_de_poderes_de_energia_possuidos"]
            self.numero_de_poderes_de_morte_possuidos = dados["numero_de_poderes_de_morte_possuidos"]
            self.numero_de_poderes_de_sangue_possuidos = dados["numero_de_poderes_de_sangue_possuidos"]

            self.xp = dados["xp"]

            self.circulo_ritual_maximo = 1

            self.pv_extra = 0
            self.pe_extra = 0
            self.sn_extra = 0
            self.define_status_extra()

            if self.nivel_de_exposicao >= 70:
                self.nivel_de_treinamento_em_pericia_maximo = "expert"
            elif self.nivel_de_exposicao >= 35:
                self.nivel_de_treinamento_em_pericia_maximo = "veterano"
            else:
                self.nivel_de_treinamento_em_pericia_maximo = "treinado"

        self.transcendeu = False

    def verifica_upou_de_nivel(self):
        if self.nivel_de_exposicao < 99:
            niveis_xp = (921, 4474, 11271, 21710, 36100, 54694, 77713, 105352,
                         137787, 175178, 217672, 265408, 318514, 377111, 441315,
                         511233, 586971, 668626, 756294)
            nivel_atual = self.nivel_de_exposicao//5
            xp_para_upar = niveis_xp[nivel_atual-1]

            if xp_para_upar <= self.xp:
                return True
            else:
                return False
        else:
            return False

    @staticmethod
    def retorna_valor_correto(numero_escolhido, lista_referente_ao_valor, diminuir=True):
        try:
            numero_escolhido = int(numero_escolhido) - 1 if diminuir else int(numero_escolhido)

        except ValueError:
            numero_escolhido = len(lista_referente_ao_valor) + 1

        while numero_escolhido >= len(lista_referente_ao_valor):
            print("erro!\n"
                  "Tente novamente\n")
            numero_escolhido = input("-> ")
            try:
                numero_escolhido = int(numero_escolhido) - 1 if diminuir else int(numero_escolhido)
            except ValueError:
                numero_escolhido = len(lista_referente_ao_valor) + 1

        return numero_escolhido

    def escolhe_trilha(self):
        if self.classe == "combatente":
            todas_as_trilhas = {"aniquilador": ["a favorita", "técnica secreta", "técnica sublime", "máquina de matar"],
                                "comandante de campo": ["inspirar confiança", "estrategista", "brecha na guarda", "oficial comandante"],
                                "guerreiro": ["técnica letal", "revidar", "força opressora", "potência máxima"],
                                "operações especiais": ["iniciativa aprimorada", "ataque extra", "surto de adrenalina", "sempre alerta"],
                                "tropa de choque": ["casca grossa", "cai dentro", "duro de matar", "inquebrável"]}

        elif self.classe == "especialista":
            todas_as_trilhas = {"atirador de elite": ["mira de elite", "disparo letal", "disparo impactante", "atirar para matar"],
                                "infiltrador": ["ataque furtivo", "gatuno", "assassinar", "sombra fugaz"],
                                "médico de campo": ["paramédico", "equipe de trauma", "resgate", "reanimação"],
                                "negociador": ["eloquência", "discurso motivador", "eu conheço um cara", "truque de mestre"],
                                "técnico": ["inventario otimizado", "remendão", "improvisar", "preparado para tudo"]}
        else:
            todas_as_trilhas = {"conduíte": ["ampliar ritual", "acelerar ritual", "anular ritual", "conhecendo o medo"],
                                "flagelador": ["poder do flagelo", "abraçar a dor", "absorver agonia", "medo tangível"],
                                "graduado": ["saber ampliado", "grimório ritualístico", "rituais eficientes", "conhecendo o medo"],
                                "intuitivo": ["mente sã", "presença poderosa", "inabalável", "presença do medo"],
                                "lâmina paranormal": ["lâmina maldita", "gladiador paranormal", "conjuração marcial", "lãmina de medo"]}

        todos_os_nomes_das_trilhas = tuple([trilha for trilha in todas_as_trilhas])
        poderes_da_trilha_escolhida = []

        if self.nivel_de_exposicao > 10:
            poderes_da_trilha_escolhida = todas_as_trilhas[self.trilha]

        if self.nivel_de_exposicao == 10:
            print(f"Escolha uma destas trilhas para {self.classe}:\n")

            index = 1
            for trilha in todas_as_trilhas:
                poderes_da_trilha_atual = todas_as_trilhas[trilha]
                print(f"{index} - {trilha}:\n"
                      f"NEX 10% -{poderes_da_trilha_atual[0]}\n"
                      f"NEX 45% -{poderes_da_trilha_atual[1]}\n"
                      f"NEX 65% -{poderes_da_trilha_atual[2]}\n"
                      f"NEX 99% -{poderes_da_trilha_atual[3]}\n")
                index += 1

            numero_trilha_escolhida = self.retorna_valor_correto(input("-> "), todos_os_nomes_das_trilhas)

            trilha_escolhida = todos_os_nomes_das_trilhas[numero_trilha_escolhida]
            poderes_da_trilha_escolhida = todas_as_trilhas[trilha_escolhida]

            self.trilha = trilha_escolhida
            self.poderes.append(poderes_da_trilha_escolhida[0])

        elif self.nivel_de_exposicao == 40:
            self.poderes.append(poderes_da_trilha_escolhida[1])

        elif self.nivel_de_exposicao == 65:
            self.poderes.append(poderes_da_trilha_escolhida[2])

        elif self.nivel_de_exposicao == 100:
            self.poderes.append(poderes_da_trilha_escolhida[3])

        # apenas ocorre se chamar com self.versatilidade()
        else:
            print(f"Escolha um desdes primeiros poderes das trilhas de {self.classe}:\n")

            todos_os_poderes_para_escolher = []
            for trilha in todas_as_trilhas:
                if trilha is not self.trilha:
                    todos_os_poderes_para_escolher.append(todas_as_trilhas[trilha][0])

            index = 1
            for poder in todos_os_poderes_para_escolher:
                print(f"{index} - {poder}")
                index += 1

            numero_poder_escolhido = self.retorna_valor_correto(input("\n-> "), todos_os_poderes_para_escolher)
            poder_escolhido = todos_os_poderes_para_escolher[numero_poder_escolhido]

            self.poderes.append(poder_escolhido)

    def escolhe_origem(self):
        todas_as_origens = {"acadêmico": ["ciências", "investigação", "saber é poder"],
                            "agente de saúde": ["intuição", "medicina", "técnica medicinal"],
                            "amnésico": ["você pode escolher duas pericias a sua escolha", "vislumbres do passado"],
                            "artista": ["artes", "enganação", "magnum 0pus"],
                            "atleta": ["acrobacia", "atletismo", "110%"],
                            "chef": ["fortitude", "prodissão", "ingrediente secreto"],
                            "criminoso": ["crime", "furtividade", "o crime compensa"],
                            "cultista arrependido": ["ocultismo", "religião", "traços do outro lado"],
                            "desgarrado": ["fortitude", "sobrevivência", "calejado"],
                            "engenheiro": ["profissão", "tecnologia", "ferramentas favoritas"],
                            "executivo": ["diplomacia", "profissão", "processo otimizado"],
                            "investigador": ["investigação", "percepção", "faro para pistas"],
                            "lutador": ["luta", "reflexos", "mão pesada"],
                            "magnata": ["diplomacia", "pilotagem", "patrocinador da ordem"],
                            "mercenário": ["iniciativa", "intimidação", "posição de combate"],
                            "militar": ["pontaria", "tática", "para bellum"],
                            "operário": ["fortitude", "profissão", "ferramentas de trabalho"],
                            "policial": ["percepção", "pontaria", "patrulha"],
                            "religioso": ["religião", "vontade", "acalentar"],
                            "servidor público": ["intuição", "vontade", "espírito cívico"],
                            "teórico da conspiração": ["investigação", "ocultismo", "eu já sabia"],
                            "t.i.": ["investigação", "tecnologia", "motor de busca"],
                            "trabalhador rural": ["adestramento", "sobrêvivencia", "desbravador"],
                            "trambiqueiro": ["crime", "enganação", "impostor"],
                            "universitário": ["atualidades", "investigação", "dedicação"],
                            "vítima": ["reflexos", "vontade", "cicatrizes psicológicas"]}
        lista_de_nomes_das_origens = tuple([origem for origem in todas_as_origens])

        print("Escolha uma origem para o seu personagem:\n")

        index = 1
        for origem in todas_as_origens:
            lista_de_informacoes_da_origem = todas_as_origens[origem]

            if origem != "amnésico":
                print(f"{index} - origem {origem}:\n"
                      f"Perícias: {lista_de_informacoes_da_origem[0]}, {lista_de_informacoes_da_origem[1]}\n"
                      f"Poder: {lista_de_informacoes_da_origem[2]}\n")
            else:
                print(f"{index} - origem {origem}:\n"
                      f"Perícias: {lista_de_informacoes_da_origem[0]}"
                      f"Poder: {lista_de_informacoes_da_origem[1]}\n")

            index += 1

        numero_da_origem_escolhida = self.retorna_valor_correto(input("-> "), lista_de_nomes_das_origens)

        origem_escolhida = lista_de_nomes_das_origens[numero_da_origem_escolhida]

        self.origem = origem_escolhida
        informacoes_da_origem_escolhida = todas_as_origens[self.origem]

        if self.origem != "amnésico":
            self.poderes.append(informacoes_da_origem_escolhida[2])
            self.treina_pericias(0, True, informacoes_da_origem_escolhida[:2])
        else:
            self.poderes.append(informacoes_da_origem_escolhida[1])
            self.treina_pericias(2)

        if self.origem == "cultista arrependido":
            self.transcende()

    def treina_pericias(self, numero_de_perciais_para_treinar=0, treina_pericia_direto=False, pericias=()):
        niveis_de_treinamento = {"destreinado": 0, "treinado": 1, "veterano": 2, "expert": 3}

        todas_as_pericias = ("acrobacia", "adestramento", "artes", "atletismo", "atualidades",
                             "ciências", "crime", "diplomacia", "enganação", "fortitude",
                             "furtividade", "iniciativa", "intimidação", "intuição", "investigação",
                             "luta", "medicina", "ocultismo", "percepção", "pilotagem",
                             "pontaria", "profissão", "reflexos", "religião", "sobrevivência",
                             "tática", "tecnologia", "vontade")

        if treina_pericia_direto:
            if self.classe == "combatente":
                for index in range(2):
                    print("Escolha entre estas duas pericias para treinar:\n")

                    if index == 0:
                        pericias = ["luta", "pontaria"]
                    else:
                        pericias = ["fortitude", "reflexos"]

                    print(f"1 - {pericias[0]}\n2 - {pericias[1]}")

                    numero_da_escolha = self.retorna_valor_correto(input("-> "), pericias)
                    escolha = pericias[numero_da_escolha]

                    self.pericias_treinadas[escolha] = "treinado"
            else:
                for pericia in pericias:
                    if pericia not in self.pericias_treinadas:
                        self.pericias_treinadas[pericia] = "treinado"
                        print("entrou no if ", pericia, self.pericias_treinadas)
                    else:
                        print("entrou no else")

                        nivel_treinamento = self.pericias_treinadas[pericia]

                        if nivel_treinamento == "expert":
                            print("*UMA PERÍCIA NÃO FOI UPADO DEVIDO AO SEU NÍVEL DE TREINAMENTO JÁ SER O MÁXIMO")
                            continue
                        elif nivel_treinamento == "veterano":
                            if niveis_de_treinamento[self.nivel_de_treinamento_em_pericia_maximo] >= niveis_de_treinamento[nivel_treinamento]:
                                self.pericias_treinadas[pericia] = "expert"
                            else:
                                print("*UMA PERÍCIA NÃO FOI UPADO DEVIDO AO SEU NÍVEL DE TREINAMENTO JÁ SER O MÁXIMO --PERMITIDO--")
                        else:
                            print("bool ", niveis_de_treinamento[self.nivel_de_treinamento_em_pericia_maximo] >= niveis_de_treinamento[nivel_treinamento])
                            print("maximo ", niveis_de_treinamento[self.nivel_de_treinamento_em_pericia_maximo], self.nivel_de_treinamento_em_pericia_maximo)
                            print("nivel pericia ", niveis_de_treinamento[nivel_treinamento], nivel_treinamento)

                            if niveis_de_treinamento[self.nivel_de_treinamento_em_pericia_maximo] > niveis_de_treinamento[nivel_treinamento]:
                                self.pericias_treinadas[pericia] = "veterano"
                            else:
                                self.treina_pericias(1)

        if not treina_pericia_direto:
            while numero_de_perciais_para_treinar > 0:

                todas_as_pericias_treinaveis = []
                for pericia in todas_as_pericias:
                    if pericia not in self.pericias_treinadas:
                        todas_as_pericias_treinaveis.append(pericia)
                    else:
                        nivel_treinamento_pericia = niveis_de_treinamento[self.pericias_treinadas[pericia]]
                        nivel_treinamento_maximo = niveis_de_treinamento[self.nivel_de_treinamento_em_pericia_maximo]
                        print(nivel_treinamento_pericia, nivel_treinamento_maximo,
                              nivel_treinamento_pericia < nivel_treinamento_maximo)

                        if nivel_treinamento_pericia < nivel_treinamento_maximo:
                            todas_as_pericias_treinaveis.append(pericia)

                print(f"Você pode treinar {numero_de_perciais_para_treinar} perícias\n"
                      f"\nEscolha uma:")

                index = 1
                for pericia in todas_as_pericias_treinaveis:
                    print(f"{index} - {pericia.capitalize()}")
                    index += 1

                numero_da_percia_escolhida = self.retorna_valor_correto(input("-> "), todas_as_pericias_treinaveis)
                pericia_escolhida = todas_as_pericias_treinaveis[numero_da_percia_escolhida]

                if pericia_escolhida not in self.pericias_treinadas:
                    self.pericias_treinadas[pericia_escolhida] = "treinado"
                    numero_de_perciais_para_treinar -= 1

                else:
                    if self.pericias_treinadas[pericia_escolhida] == "treinado":
                        self.pericias_treinadas[pericia_escolhida] = "veterano"
                        numero_de_perciais_para_treinar -= 1

                    elif self.pericias_treinadas[pericia_escolhida] == "veterano":
                        self.pericias_treinadas[pericia_escolhida] = "expert"
                        numero_de_perciais_para_treinar -= 1

    def cria_e_melhora_atributos(self, pontos_de_atributo=1, criando_atributos=False, sem_limite=False):
        atributos = ("agilidade", "força", "intelecto", "presença", "vigor")

        if criando_atributos:
            print("Você vai diminuir algum atributo a zero para receber um ponto extra para distribuição?\n"
                  "[Digite 'sim' para diminuir ou 'não' para não diminuir]\n")
            diminuir_atributo = input("-> ").lower()

            if diminuir_atributo != "sim" and diminuir_atributo != "não":
                diminuir_atributo = "erro"

                while diminuir_atributo == "erro":
                    diminuir_atributo = input("-> ").lower()

                    if diminuir_atributo != "sim" and diminuir_atributo != "não":
                        diminuir_atributo = "erro"

            if diminuir_atributo == "sim":
                pontos_de_atributo += 1
                self.atributos[self.diminui_atributo()] -= 1

            print("\nEscolha quais atributos você quer melhorar:\n")
            index = 1
            while pontos_de_atributo > 0:
                if index == 1:
                    for atributo in atributos:
                        print(f"{index} - {atributo}")
                        index += 1

                atributo_escolhido = self.retorna_valor_correto(input("\n-> "), atributos)

                if self.atributos[atributos[atributo_escolhido]] < 3:
                    self.atributos[atributos[atributo_escolhido]] += 1
                    pontos_de_atributo -= 1
                    print("ok!")
                else:
                    print(f"você não pode ultrapassar 3 pontos em nenhum atributo durante a criação de personagem.\n"
                          f"Lhe restam {pontos_de_atributo} pontos de atributo.\n")
                    continue
        else:
            if pontos_de_atributo == 1:
                print("\nEscolha qual atributos você quer melhorar:\n")
            else:
                print("\nEscolha quais atributos você quer melhorar:\n")

            index = 1
            while pontos_de_atributo > 0:
                if index == 1:
                    for atributo in atributos:
                        print(f"{index} - {atributo}")
                        index += 1

                atributo_escolhido = self.retorna_valor_correto(input("\n-> "), atributos)

                if sem_limite:
                    self.atributos[atributos[atributo_escolhido]] += 1
                    pontos_de_atributo -= 1
                    print("ok!\n")

                elif self.atributos[atributos[atributo_escolhido]] < 5:
                    self.atributos[atributos[atributo_escolhido]] += 1
                    pontos_de_atributo -= 1
                    print("ok!\n")

                else:
                    print(f"você não pode ultrapassar 5 pontos em nenhum atributo com este metodo.\n"
                          f"Lhe restam {pontos_de_atributo} pontos de atributo.\n")
                    continue

    def diminui_atributo(self):
        atributos = ("agilidade", "força", "intelecto", "presença", "vigor")

        print("Escolha um:")
        index = 1
        for atributo in atributos:
            print(f"{index} - {atributo}")
            index += 1

        atributo_escolhido = self.retorna_valor_correto(input("-> "), atributos)

        return atributos[atributo_escolhido]

    def aumenta_nivel_de_exposicao(self):
        self.nivel_de_exposicao += 5
        self.atualiza_status_extra()
        self.atualiza_atributos()
        self.atualiza_nivel_de_treinamento_maximo()
        self.recebe_beneficios_do_nivel_de_exposicao()
        self.atualiza_atributos()

        self.atualiza_banco_de_dados()

    def sobe_nex_ate_um_valor_determinado(self, valor_desejado):
        if not str(valor_desejado).endswith("5") and not str(valor_desejado).endswith("0"):
            print("valor inválido1")
            return
        elif self.nivel_de_exposicao - valor_desejado >= 5:
            print("valor inválido2")
            vezes_para_upar = 0
        else:
            vezes_para_upar = abs(self.nivel_de_exposicao - valor_desejado) // 5

        for _ in range(vezes_para_upar):
            self.aumenta_nivel_de_exposicao()

    def define_status_extra(self):
        dict_status_extra = {"pv": 0,
                             "pe": 0,
                             "sn": 0}

        modificadores = {"calejado": ["pv", "5"],
                         "dedicação": ["pe", "1.5 + nex/10"],
                         "cicatrizes psicológicas": ["sn", "5"],
                         "potencial aprimorado": ["pe", "5"],
                         "potencial aprimorado (afinidade)": ["pe", "5"],
                         "sangue de ferro": ["pv", "5"],
                         "sangue de ferro (afinidade)": ["pv", "5"],
                         "casca grossa": ["pv", "5"]}

        for poder in modificadores:
            if poder in self.poderes:
                if poder == "dedicação":
                    dict_status_extra["pe"] += round(1.5 + self.nivel_de_exposicao / 10)
                else:
                    status_modificar = modificadores[poder][0]
                    fator_de_calculo = float(modificadores[poder][1])

                    dict_status_extra[status_modificar] += round(self.nivel_de_exposicao / fator_de_calculo)

        self.pv_extra = dict_status_extra["pv"]
        self.pe_extra = dict_status_extra["pe"]
        self.sn_extra = dict_status_extra["sn"]

    def atualiza_status_extra(self):
        self.vida -= self.pv_extra
        self.pontos_de_esforco -= self.pe_extra
        self.sanidade -= self.sn_extra

        self.define_status_extra()

        self.vida += self.pv_extra
        self.pontos_de_esforco += self.pe_extra
        self.sanidade += self.sn_extra

    def recebe_beneficios_do_nivel_de_exposicao(self):
        self.transcendeu = False

        if self.nivel_de_exposicao == 5:
            self.escolhe_classe()
            self.recebe_poderes()

            if self.classe == "combatente":
                self.treina_pericias(0, True)
                pericias_para_treinar = 1 + self.intelecto

            elif self.classe == "especialista":
                pericias_para_treinar = 7 + self.intelecto

            else:
                self.treina_pericias(0, True, ("ocultismo", "vontade"))
                pericias_para_treinar = 3 + self.intelecto

            self.treina_pericias(pericias_para_treinar)

        elif self.nivel_de_exposicao == 10:
            self.escolhe_trilha()
            if "saber ampliado" in self.poderes:
                self.aprende_ritual()

            if "lâmina maldita" in self.poderes:
                rituais_de_amaldicoar_arma = ("amaldiçoar arma com conhecimento", "amaldiçoar arma com energia",
                                              "amaldiçoar arma com morte", "amaldiçoar arma com sangue")

                for ritual in rituais_de_amaldicoar_arma:
                    if ritual in self.rituais:
                        self.poderes.remove(ritual + " (círculo 1)")
                        self.poderes.append(ritual + " (círculo 1) *custo reduzido por lâmina maldita")

                else:
                    self.aprende_ritual(False, True)

        elif self.nivel_de_exposicao == 15:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 20:
            self.cria_e_melhora_atributos()

        elif self.nivel_de_exposicao == 25:
            if "saber ampliado" in self.poderes:
                self.aprende_ritual()

        elif self.nivel_de_exposicao == 30:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 35:
            if self.classe == "combatente":
                pericias_para_treinar = 2 + self.intelecto

            elif self.classe == "especialista":
                pericias_para_treinar = 5 + self.intelecto

            else:
                pericias_para_treinar = 3 + self.intelecto

            self.treina_pericias(pericias_para_treinar)

        elif self.nivel_de_exposicao == 40:
            self.escolhe_trilha()
            if self.trilha == "graduado":
                for _ in range(self.intelecto):
                    self.aprende_ritual(False, False, True)

        elif self.nivel_de_exposicao == 45:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 50:
            self.define_afinidade()
            self.cria_e_melhora_atributos()
            self.versatilidade()

        elif self.nivel_de_exposicao == 55:
            if "saber ampliado" in self.poderes:
                self.aprende_ritual()
                self.aprende_ritual(False, False, True)

        elif self.nivel_de_exposicao == 60:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 65:
            self.escolhe_trilha()

        elif self.nivel_de_exposicao == 70:
            if self.classe == "combatente":
                pericias_para_treinar = 2 + self.intelecto

            elif self.classe == "especialista":
                pericias_para_treinar = 5 + self.intelecto

            else:
                pericias_para_treinar = 3 + self.intelecto

            self.treina_pericias(pericias_para_treinar)

        elif self.nivel_de_exposicao == 75:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 80:
            self.cria_e_melhora_atributos()

        elif self.nivel_de_exposicao == 85:
            if "saber ampliado" in self.poderes:
                self.aprende_ritual()
                self.aprende_ritual(False, False, True)

        elif self.nivel_de_exposicao == 90:
            self.recebe_poderes()

        elif self.nivel_de_exposicao == 95:
            self.cria_e_melhora_atributos()

        elif self.nivel_de_exposicao == 100:
            self.escolhe_trilha()
            if self.classe == "ocultista":
                self.aprende_ritual(False, True)

        if not self.transcendeu:
            self.aumenta_sanidade()
        self.aumenta_vida()
        self.aumenta_pontos_de_esforco()

        if self.classe == "ocultista":
            self.aprende_ritual(True)

    def __str__(self):
        pericias_formatadas = ""
        rituais_formatados = ""
        poderes_formatados = ""

        for pericia in self.pericias_treinadas:
            pericias_formatadas += f"{pericia} - {self.pericias_treinadas[pericia]}\n"

        for poder in self.poderes:
            if "círculo" in poder:
                rituais_formatados += f"{poder}\n"
            else:
                poderes_formatados += f"{poder}\n"

        nex = self.nivel_de_exposicao if self.nivel_de_exposicao < 100 else self.nivel_de_exposicao - 1

        return f"NOME - {self.nome}\n"\
              f"\n"\
              f"             {self.agilidade}\n"\
              f"            AGI\n"\
              f"     {self.forca}               {self.intelecto}\n"\
              f"    FOR             INT\n"\
              f"\n"\
              f"        {self.presenca}         {self.vigor}\n"\
              f"       PRE       VIG\n"\
              f"\n"\
              f"ORIGEM - {self.origem}\n"\
              f"CLASSE - {self.classe} | {self.trilha}\n"\
              f"NEX - {nex}%\n"\
              f"PV - {self.vida}  |  PE - {self.pontos_de_esforco}\n"\
              f"SAN - {self.sanidade}\n"\
              f"\n"\
              f"PERÍCIAS:\n"\
              f"\n"\
              f"{pericias_formatadas}"\
              f"\n"\
              f"RITUAIS:\n"\
              f"\n"\
              f"{rituais_formatados}"\
              f"\n"\
              f"PODERES:\n"\
              f"\n"\
              f"{poderes_formatados}"

    def custo_poder(self, poder):
        dict_custo_poder = requests.get(f"{self.banco_dados}/info/poderes/.json").json()

        try:
            custo = dict_custo_poder[poder][0]
        except KeyError:
            custo = "0pe"

        return custo

    def define_afinidade(self):
        elementos = ("conhecimento", "energia", "morte", "sangue")

        print(f"Escolha um destes elementos para receber afinidade com:\n")

        index = 1
        for elemento in elementos:
            print(f"{index} - {elemento}")
            index += 1

        numero_do_elemento_escolhido = self.retorna_valor_correto(input("\n-> "), elementos)

        elemento_escolhido = elementos[numero_do_elemento_escolhido]

        self.afinidade = elemento_escolhido

    def versatilidade(self):
        escolhas = ("poder de classe", "poder de trilha")
        print(f"Escolha entre receber um poder de {self.classe} ou o primeiro poder de qualquer trilha da sua classe:\n")

        index = 1
        for escolha in escolhas:
            print(f"{index} - {escolha}")
            index += 1

        numero_da_escolha = self.retorna_valor_correto(input("\n-> "), escolhas)

        escolha = escolhas[numero_da_escolha]

        if escolha == "poder de classe":
            self.escolhe_poderes()
        else:
            self.escolhe_trilha()

    def recebe_poderes(self):
        niveis_ganha_poder = (15, 30, 45, 60, 75, 90)

        if self.nivel_de_exposicao == 5:

            if self.classe == "combatente":
                self.poderes.append("ataque especial")

            elif self.classe == "especialista":
                self.poderes.append("eclético")
                self.poderes.append("perito")

            else:
                self.poderes.append("escolhido pelo Outro Lado")

        elif self.nivel_de_exposicao in niveis_ganha_poder:
            self.escolhe_poderes()

        elif self.classe == "especialista" and self.nivel_de_exposicao == 40:
            self.poderes.append("engenhosidade")

    def escolhe_poderes(self, escolhendo_por_expansao_de_conhecimento=False):
        todas_classes_dos_poderes = ["combatente", "especialista", "ocultista"]
        classes_dos_poderes = []
        poderes_de_classe = {}

        if not escolhendo_por_expansao_de_conhecimento:
            classes_dos_poderes.append(self.classe)
        else:
            for classe in todas_classes_dos_poderes:
                if classe != self.classe:
                    classes_dos_poderes.append(classe)

        if "combatente" in classes_dos_poderes:
            poderes_de_classe["combatente"] = {"armamento pesado": ["força-2", "", ""],
                                               "arte marcial": ["", "", ""],
                                               "ataque de oportunidade": ["", "", ""],
                                               "combater com duas armas": ["agilidade-3", "", "luta|pontaria"],
                                               "combate defensivo": ["intelecto-2", "", ""],
                                               "golpe demolidor": ["força-2", "", "luta"],
                                               "golpe pesado": ["", "", ""],
                                               "incansável": ["", "", ""],
                                               "presteza atlética": ["", "", ""],
                                               "proteção pesada": ["", 30, ""],
                                               "reflexos defensivos": ["agilidade-2", "", ""],
                                               "saque rápido": ["", "", "iniciativa"],
                                               "segurar gatilho": ["", 60, ""],
                                               "sentido tático": ["intelecto-2", "", "percepção tática"],
                                               "tanque de guerra": ["*", "", ""],
                                               "tiro certeiro": ["", "", "pontaria"],
                                               "tiro de cobertura": ["", "", ""],
                                               "treinamento em perícia": ["", "", ""],
                                               "transcender": ["", "", ""]}

        if "especialista" in classes_dos_poderes:
            poderes_de_classe["especialista"] = {"arte marcial": ["", "", ""],
                                                 "balística avançada": ["", "", ""],
                                                 "conhecimento ampliado": ["intelecto-2", "", ""],
                                                 "hacker": ["", "", "tecnologia"],
                                                 "mãos rápidas": ["agilidade-3", "", "crime"],
                                                 "mochila de utilidades": ["", "", ""],
                                                 "movimento tático": ["", "", "atletismo"],
                                                 "na trilha certa": ["", "", ""],
                                                 "nerd": ["", "", ""],
                                                 "ninja urbano": ["", "", ""],
                                                 "pensamento ágil": ["", "", ""],
                                                 "perito em explosivos": ["", "", ""],
                                                 "primeira impressão": ["", "", ""],
                                                 "treinamento em perícia": ["", "", ""],
                                                 "transcender": ["", "", ""]}

        if "ocultista" in classes_dos_poderes:
            poderes_de_classe["ocultista"] = {"camuflar ocultismo": ["", "", ""],
                                              "criar selo": ["", "", ""],
                                              "envolto em mistério": ["", "", ""],
                                              "especialista em elemento": ["", "", ""],
                                              "ferramentas paranormais": ["", "", ""],
                                              "fluxo de poder": ["", 60, ""],
                                              "guiado pelo paranormal": ["", "", ""],
                                              "indentificação paranormal": ["", "", ""],
                                              "improvisar componentes": ["", "", ""],
                                              "intuição paranormal": ["", "", ""],
                                              "mestre em elemento": ["*", "", ""],
                                              "ritual potente": ["intelecto-2", "", ""],
                                              "ritual predileto": ["", "", ""],
                                              "tatuagem ritualística": ["", "", ""],
                                              "treinamento em perícia":  ["", "", ""],
                                              "transcender": ["", "", ""]}

        poderes_especificos = ("tanque de guerra", "mestre em elemento", "transcender", "treinamento em perícia")
        poderes_comuns_entre_todas_as_classes = ("transcender", "treinamento em perícia")

        poderes_de_classe_para_escolher = {}

        for classe in poderes_de_classe:
            for poder in poderes_de_classe[classe]:
                if poder not in self.poderes and poder not in poderes_de_classe_para_escolher:
                    if escolhendo_por_expansao_de_conhecimento:
                        if poder not in poderes_comuns_entre_todas_as_classes:
                            poderes_de_classe_para_escolher[poder] = poderes_de_classe[classe][poder]
                    else:
                        poderes_de_classe_para_escolher[poder] = poderes_de_classe[classe][poder]

        todos_nomes_de_poder_para_escolher = tuple([poder for poder in poderes_de_classe_para_escolher])
        escolheu_poder = False

        while not escolheu_poder:
            print("Escolha um destes poderes de classe:\n")

            index = 1
            for poder in todos_nomes_de_poder_para_escolher:
                print(f"{index} - {poder}")
                index += 1

            numero_do_poder_escolhido = self.retorna_valor_correto(input("-> "), todos_nomes_de_poder_para_escolher)

            poder_escolhido = todos_nomes_de_poder_para_escolher[numero_do_poder_escolhido]
            requisitos_do_poder = poderes_de_classe_para_escolher[poder_escolhido]

            if poder_escolhido in self.poderes:
                print("\nVocê já possui este poder!")
                continue

            if poder_escolhido not in poderes_especificos:
                index = 1
                nao_atendeu_requisito = False

                for requisito in requisitos_do_poder:
                    if requisito != "" and index == 1:
                        separador_nome = requisito.find("-")
                        separador_valor = requisito.find("-") + 1
                        atributo_do_requisito = requisito[:separador_nome]
                        valor_do_requisito = int(requisito[separador_valor:])

                        if self.atributos[atributo_do_requisito] < valor_do_requisito:
                            nao_atendeu_requisito = True
                            break

                    elif requisito != "" and index == 2:
                        if self.nivel_de_exposicao < requisito:
                            nao_atendeu_requisito = True
                            break

                    elif requisito != "" and index == 3:
                        pericias_requisitadas = requisito.split()

                        for pericia in pericias_requisitadas:
                            if "|" in pericia:
                                pericia_1 = pericia.split("|")[0]
                                pericia_2 = pericia.split("|")[1]
                                if pericia_1 not in self.pericias_treinadas and pericia_2 not in self.pericias_treinadas:
                                    nao_atendeu_requisito = True
                                    break

                            if pericia not in self.pericias_treinadas:
                                nao_atendeu_requisito = True
                                break

                    index += 1
                    # acabou o for

                if nao_atendeu_requisito:
                    print("\nVocê não atende os requisitos deste poder!")
                    continue
                else:
                    self.poderes.append(poder_escolhido)
                    escolheu_poder = True
                # acabou checagem dos poderes normais

            nao_atendeu_requisito = False
            if poder_escolhido == "tanque de guerra":
                if "proteção pesada" in self.poderes:
                    self.poderes.append(poder_escolhido)
                    escolheu_poder = True
                else:
                    nao_atendeu_requisito = True

            elif poder_escolhido == "mestre em elemento":
                if "especialista em elemento" in self.poderes and self.nivel_de_exposicao >= 45:
                    self.poderes.append(poder_escolhido)
                    escolheu_poder = True
                else:
                    nao_atendeu_requisito = True

            elif poder_escolhido == "transcender":
                self.transcendeu = True
                self.transcende()
                escolheu_poder = True

            elif poder_escolhido == "treinamento em perícia":
                self.treina_pericias(2)
                escolheu_poder = True

            if nao_atendeu_requisito:
                print("\nVocê não atende os requisitos deste poder!")
                continue

    def transcende(self):
        recebeu_poder = False

        poderes_de_elemento_variado_para_escolher = {"aprender ritual": 0}

        poderes_de_conhecimento_para_escolher = {"resistir à conhecimento": 0,
                                                 "expansão de conhecimento": 1,
                                                 "percepção paranormal": 0,
                                                 "precognição": 1,
                                                 "sensitivo": 0,
                                                 "visão do oculto": 0}

        poderes_de_energia_para_escolher = {"resistir à energia": 0,
                                            "afortunado": 0,
                                            "campo protetor": 1,
                                            "casualidade fortuita": 0,
                                            "golpe de sorte": 1,
                                            "manipular entropia": 0}

        poderes_de_morte_para_escolher = {"resistir à morte": 0,
                                          "encarar a morte": 0,
                                          "escapar da morte": 1,
                                          "potencial aprimorado": 0,
                                          "potencial reaproveitado": 0,
                                          "surto temporal": 2}

        poderes_de_sangue_para_escolher = {"resistir à sangue": 0,
                                           "anatomia insana": 2,
                                           "arma de sangue": 0,
                                           "sangue de ferro": 0,
                                           "sangue fervente": 2,
                                           "sangue vivo": 1}

        todos_os_poderes = {"elemento variado": poderes_de_elemento_variado_para_escolher,
                            "conhecimento": poderes_de_conhecimento_para_escolher,
                            "energia": poderes_de_energia_para_escolher,
                            "morte": poderes_de_morte_para_escolher,
                            "sangue": poderes_de_sangue_para_escolher}

        poderes_com_afinidade = {}

        for elemento in todos_os_poderes:

            for poder_do_elemento in todos_os_poderes[elemento]:
                poder_com_afinidade = poder_do_elemento + " (afinidade)"

                if poder_com_afinidade in self.poderes:
                    if elemento not in poderes_com_afinidade:
                        poderes_com_afinidade[elemento] = []

                    poderes_com_afinidade[elemento].append(poder_do_elemento)

        for elemento in poderes_com_afinidade:
            for poder in poderes_com_afinidade[elemento]:
                del todos_os_poderes[elemento][poder]

        elementos = {1: "elemento variado", 2: "conhecimento", 3: "energia", 4: "morte", 5: "sangue"}

        numero_de_poderes_de_elemento_variado = len(poderes_de_elemento_variado_para_escolher)

        while not recebeu_poder:
            print("Escolha um poder de:")

            todos_os_nomes_dos_poderes = []

            index = 1
            for elemento_dos_poderes in todos_os_poderes:
                print(f"{elemento_dos_poderes.capitalize()}:\n")

                poderes = todos_os_poderes[elemento_dos_poderes]

                for poder in poderes:
                    todos_os_nomes_dos_poderes.append(poder)
                    print(f"{index} - {poder.capitalize()}")
                    index += 1
                print("\n", end="")

            numero_do_poder_escolhido = self.retorna_valor_correto(input("-> "), todos_os_nomes_dos_poderes)

            numero_elemento = 1 if numero_do_poder_escolhido < numero_de_poderes_de_elemento_variado else 2

            if numero_elemento != 1:
                numero_do_poder_escolhido -= numero_de_poderes_de_elemento_variado

                while numero_do_poder_escolhido > 5:
                    numero_do_poder_escolhido -= 6
                    numero_elemento += 1

            elemento = elementos[numero_elemento]
            poderes_do_elemento_escolhido = tuple(todos_os_poderes[elemento])
            escolha = poderes_do_elemento_escolhido[numero_do_poder_escolhido]

            if elemento == "elemento variado":
                if escolha == "aprender ritual" and self.limite_de_rituais_para_aprender > len(self.rituais):
                    self.aprende_ritual()
                    recebeu_poder = True
                else:
                    print("Você atingiu o máximo de rituais que pode ter com esta quantidade de intelecto!")

            elif elemento == "conhecimento":
                if poderes_de_conhecimento_para_escolher[escolha] > self.numero_de_poderes_de_conhecimento_possuidos:
                    print("Você não atende os pré-requisitos deste poder!\n")

                elif escolha not in self.poderes:
                    self.poderes.append(escolha)
                    self.numero_de_poderes_de_conhecimento_possuidos += 1
                    recebeu_poder = True

                elif self.afinidade == "conhecimento":
                    self.poderes.append(escolha + " (afinidade)")
                    recebeu_poder = True

                else:
                    print("Você já possui este poder e não pode receber afinidade com ele!\n")

            elif elemento == "energia":
                if poderes_de_energia_para_escolher[escolha] > self.numero_de_poderes_de_energia_possuidos:
                    print("Você não atende os pré-requisitos deste poder!\n")

                elif escolha not in self.poderes:
                    self.poderes.append(escolha)
                    self.numero_de_poderes_de_energia_possuidos += 1
                    recebeu_poder = True

                elif self.afinidade == "energia":
                    self.poderes.append(escolha + " (afinidade)")
                    recebeu_poder = True

                else:
                    print("Você já possui este poder e não pode receber afinidade com ele!\n")

            elif elemento == "morte":
                if poderes_de_morte_para_escolher[escolha] > self.numero_de_poderes_de_morte_possuidos:
                    print("Você não atende os pré-requisitos deste poder!\n")

                elif escolha not in self.poderes:
                    self.poderes.append(escolha)
                    self.numero_de_poderes_de_morte_possuidos += 1
                    recebeu_poder = True

                elif self.afinidade == "morte":
                    self.poderes.append(escolha + " (afinidade)")
                    recebeu_poder = True

                else:
                    print("Você já possui este poder e não pode receber afinidade com ele!\n")

            elif elemento == "sangue":
                if poderes_de_sangue_para_escolher[escolha] > self.numero_de_poderes_de_sangue_possuidos:
                    print("Você não atende os pré-requisitos deste poder!\n")

                elif escolha not in self.poderes:
                    self.poderes.append(escolha)
                    self.numero_de_poderes_de_sangue_possuidos += 1
                    recebeu_poder = True

                elif self.afinidade == "sangue":
                    self.poderes.append(escolha + " (afinidade)")
                    recebeu_poder = True

                else:
                    print("Você já possui este poder e não pode receber afinidade com ele!\n")

            if recebeu_poder and escolha == "expansão de conhecimento":
                self.escolhe_poderes(True)

    def aprende_ritual(self, aprendendo_por_escolhido_pelo_outro_lado=False, aprendendo_por_trilha_de_ocultista=False, aprendendo_por_grimorio_ritualistico=False):
        rituais_para_aprender = 1
        elementos = ("conhecimento", "energia", "morte", "sangue", "medo")

        if aprendendo_por_escolhido_pelo_outro_lado and self.nivel_de_exposicao == 5:
            rituais_para_aprender = 3

        self.atualiza_circulo_maximo()

        if aprendendo_por_trilha_de_ocultista:
            if self.trilha == "lâmina paranormal" and self.nivel_de_exposicao == 10:
                rituais_para_escolher = ("amaldiçoar arma com conhecimento", "amaldiçoar arma com energia",
                                         "amaldiçoar arma com morte", "amaldiçoar arma com sangue")

                print("Escolha um destes rituais:\n")

                index = 1
                for ritual in rituais_para_escolher:
                    print(f"{index} - {ritual}")
                    index += 1

                numero_do_ritual_escolhido = self.retorna_valor_correto(input("-> "), rituais_para_escolher)
                ritual_escolhido = rituais_para_escolher[numero_do_ritual_escolhido]

                self.rituais.append(ritual_escolhido + " (círculo 1)")

            elif self.nivel_de_exposicao == 100:
                if self.trilha == "conduíte":
                    ritual_de_trilha_para_aprender = 'canalizar o medo'
                elif self.trilha == "graduado":
                    ritual_de_trilha_para_aprender = 'conhecendo o medo'
                elif self.trilha == "lâmina paranormal":
                    ritual_de_trilha_para_aprender = 'lâmina do medo'
                elif self.trilha == "flagelador":
                    ritual_de_trilha_para_aprender = 'medo tangível'
                else:
                    ritual_de_trilha_para_aprender = 'presença do medo'

                self.poderes.append(ritual_de_trilha_para_aprender + " (círculo 4)")

        else:
            todos_os_rituais = requests.get(f"{self.banco_dados}/info/rituais/.json").json()

            while rituais_para_aprender > 0:
                todos_os_rituais_para_escolher = []

                for ritual in todos_os_rituais:
                    if ritual not in self.rituais:
                        circulo = int(todos_os_rituais[ritual][0][0])
                        if circulo <= self.circulo_ritual_maximo:
                            todos_os_rituais_para_escolher.append(ritual)

                todos_os_rituais_para_escolher = tuple(todos_os_rituais_para_escolher)

                print("Escolha um destes rituais:\n")

                index = 1
                for ritual in todos_os_rituais_para_escolher:
                    print(f"{index} - {ritual}")
                    index += 1

                if aprendendo_por_grimorio_ritualistico:
                    print("*este ritual será adicionado ao seu grimório ritualistico")

                numero_do_ritual_escolhido = self.retorna_valor_correto(input("-> "), todos_os_rituais_para_escolher)
                ritual_escolhido = todos_os_rituais_para_escolher[numero_do_ritual_escolhido]

                rituais_para_aprender -= 1
                if aprendendo_por_escolhido_pelo_outro_lado:
                    self.limite_de_rituais_para_aprender += 1

                info_ritual = todos_os_rituais[ritual_escolhido]
                circulo_ritual = info_ritual[0][:1]
                elemento = info_ritual[1]

                if not aprendendo_por_escolhido_pelo_outro_lado:
                    if elemento == "conhecimento":
                        self.numero_de_poderes_de_conhecimento_possuidos += 1

                    elif elemento == "energia":
                        self.numero_de_poderes_de_energia_possuidos += 1

                    elif elemento == "morte":
                        self.numero_de_poderes_de_morte_possuidos += 1

                    elif elemento == "sangue":
                        self.numero_de_poderes_de_sangue_possuidos += 1

                if aprendendo_por_grimorio_ritualistico:
                    self.poderes.append(ritual_escolhido + f" (círculo {circulo_ritual} - grimório ritualístico)")
                else:
                    self.poderes.append(ritual_escolhido + f" (círculo {circulo_ritual})")

                self.rituais.append(ritual_escolhido)

    def aumenta_sanidade(self):
        if self.classe == "combatente":
            if self.nivel_de_exposicao == 5:
                self.sanidade += 12 + 3
            else:
                self.sanidade += 3

            if self.origem == "cultista arrependido":
                self.sanidade = self.sanidade//2

        elif self.classe == "especialista":
            if self.nivel_de_exposicao == 5:
                self.sanidade += 16 + 4
            else:
                self.sanidade += 4

            if self.origem == "cultista arrependido":
                self.sanidade = self.sanidade//2

        else:
            if self.nivel_de_exposicao == 5:
                self.sanidade += 20 + 5
            else:
                self.sanidade += 5

            if self.origem == "cultista arrependido":
                self.sanidade = self.sanidade//2

    def aumenta_pontos_de_esforco(self):
        if self.classe == "combatente":
            if self.nivel_de_exposicao == 5:
                self.pontos_de_esforco += 4 + 2*self.presenca
            else:
                self.pontos_de_esforco += self.presenca + 2

        elif self.classe == "especialista":
            if self.nivel_de_exposicao == 5:
                self.pontos_de_esforco += 6 + 2*self.presenca
            else:
                self.pontos_de_esforco += self.presenca + 3

        else:
            if self.nivel_de_exposicao == 5:
                self.pontos_de_esforco += 8 + 2*self.presenca
            else:
                self.pontos_de_esforco += self.presenca + 4

    def aumenta_vida(self):
        if self.classe == "combatente":
            if self.nivel_de_exposicao == 5:
                self.vida += 24 + 2*self.vigor
            else:
                self.vida += self.vigor + 4

        elif self.classe == "especialista":
            if self.nivel_de_exposicao == 5:
                self.vida += 19 + 2*self.vigor
            else:
                self.vida += self.vigor + 3

        else:
            if self.nivel_de_exposicao == 5:
                self.vida += 14 + 2*self.vigor
            else:
                self.vida += self.vigor + 2

    def escolhe_classe(self):
        classes = ("combatente", "especialista", "ocultista")

        print("Escolha uma destas classes:\n")
        index = 1
        for classe in classes:
            print(f"{index} - {classe}")
            index += 1

        escolha = input("\n-> ")
        escolha = self.retorna_valor_correto(escolha, classes)

        self.classe = classes[escolha]

    def atualiza_atributos(self):
        soma_atributos_str = self.agilidade + self.forca + self.intelecto + self.presenca + self.vigor
        soma_atributos_dict = self.atributos["agilidade"] + self.atributos["força"] + self.atributos["intelecto"] + self.atributos["presença"] + self.atributos["vigor"]

        if soma_atributos_str >= soma_atributos_dict:
            self.atributos["agilidade"] = self.agilidade
            self.atributos["força"] = self.forca
            self.atributos["intelecto"] = self.intelecto
            self.atributos["presença"] = self.presenca
            self.atributos["vigor"] = self.vigor

        else:
            self.agilidade = self.atributos["agilidade"]
            self.forca = self.atributos["força"]
            self.intelecto = self.atributos["intelecto"]
            self.presenca = self.atributos["presença"]
            self.vigor = self.atributos["vigor"]

    def formata_pericias(self):
        pericias_formatado = {}
        for pericia in self.pericias_lista:
            if pericia not in self.pericias_treinadas:
                pericias_formatado[pericia] = "nt"
            else:
                if self.pericias_treinadas[pericia] == "treinado":
                    pericias_formatado[pericia] = "t"
                elif self.pericias_treinadas[pericia] == "veterano":
                    pericias_formatado[pericia] = "v"
                elif self.pericias_treinadas[pericia] == "expert":
                    pericias_formatado[pericia] = "e"

        return pericias_formatado

    def formata_poderes(self):
        poderes_formatado = {}
        for poder in self.poderes:
            if "(círculo" not in poder:
                poderes_formatado[poder] = self.custo_poder(poder)

        return poderes_formatado

    def formata_rituais(self):
        rituais_formatado = {}
        for poder in self.poderes:
            if "(círculo" in poder:
                ritual = poder.split(" (")[0]
                circulo = poder.split("círculo ")[1].replace(")", "")
                circulo += "círculo"

                rituais_formatado[ritual] = circulo

        if not rituais_formatado:
            rituais_formatado = ""

        return rituais_formatado

    def atualiza_nivel_de_treinamento_maximo(self):
        if self.nivel_de_exposicao >= 70:
            self.nivel_de_treinamento_em_pericia_maximo = "expert"
        elif self.nivel_de_exposicao >= 35:
            self.nivel_de_treinamento_em_pericia_maximo = "veterano"
        else:
            self.nivel_de_treinamento_em_pericia_maximo = "treinado"

    def atualiza_circulo_maximo(self):
        if self.classe != "ocultista":
            if self.nivel_de_exposicao >= 75:
                self.circulo_ritual_maximo = 3

            elif self.nivel_de_exposicao >= 45:
                self.circulo_ritual_maximo = 2
        else:
            if self.nivel_de_exposicao >= 85:
                self.circulo_ritual_maximo = 4

            elif self.nivel_de_exposicao >= 55:
                self.circulo_ritual_maximo = 3

            elif self.nivel_de_exposicao >= 25:
                self.circulo_ritual_maximo = 2

    def atualiza_banco_de_dados(self):
        pericias_formatado = self.formata_pericias()
        poderes_formatado = self.formata_poderes()
        rituais_formatado = self.formata_rituais()

        if self.novo:
            dados_personagens = {f"{self.nome}": {
                "anotações": "",
                "atributos": {
                    "agi": self.agilidade,
                    "for": self.forca,
                    "int": self.intelecto,
                    "pre": self.presenca,
                    "vig": self.vigor},
                "classe": self.classe,
                "defesa": 15 + self.agilidade if self.classe != "ocultista" else 10 + self.agilidade,
                "inventario": {"arma": "0 I"},
                "nex": self.nivel_de_exposicao,
                "origem": self.origem,
                "pericias": pericias_formatado,
                "poderes": poderes_formatado,
                "rituais": rituais_formatado,
                "trilha": self.trilha,
                "pv": {"maximo": self.vida, "atual": self.vida},
                "pe": {"maximo": self.pontos_de_esforco, "atual": self.pontos_de_esforco},
                "sn": {"maximo": self.sanidade, "atual": self.sanidade},
                "numero_de_poderes_de_conhecimento_possuidos": self.numero_de_poderes_de_conhecimento_possuidos,
                "numero_de_poderes_de_energia_possuidos": self.numero_de_poderes_de_energia_possuidos,
                "numero_de_poderes_de_morte_possuidos": self.numero_de_poderes_de_morte_possuidos,
                "numero_de_poderes_de_sangue_possuidos": self.numero_de_poderes_de_sangue_possuidos,
                "afinidade": self.afinidade,
                "xp": 0,
                "ultimo_xp_ganho": 0,
                "limite_rituais": self.limite_de_rituais_para_aprender}}

            dados_nomes = {f"{self.nome}": False}

            requests.patch(f"{self.banco_dados}/personagens/.json", data=json.dumps(dados_personagens))
            requests.patch(f"{self.banco_dados}/nomes/.json", data=json.dumps(dados_nomes))

            self.novo = False

        else:
            dados = {"atributos": {
                "agi": self.agilidade,
                "for": self.forca,
                "int": self.intelecto,
                "pre": self.presenca,
                "vig": self.vigor},
                "defesa": 15 + self.agilidade if self.classe != "ocultista" else 10 + self.agilidade,
                "nex": self.nivel_de_exposicao,
                "pericias": pericias_formatado,
                "poderes": poderes_formatado,
                "rituais": rituais_formatado,
                "trilha": self.trilha,
                "pv": {"maximo": self.vida, "atual": self.vida},
                "pe": {"maximo": self.pontos_de_esforco, "atual": self.pontos_de_esforco},
                "sn": {"maximo": self.sanidade, "atual": self.sanidade},
                "numero_de_poderes_de_conhecimento_possuidos": self.numero_de_poderes_de_conhecimento_possuidos,
                "numero_de_poderes_de_energia_possuidos": self.numero_de_poderes_de_energia_possuidos,
                "numero_de_poderes_de_morte_possuidos": self.numero_de_poderes_de_morte_possuidos,
                "numero_de_poderes_de_sangue_possuidos": self.numero_de_poderes_de_sangue_possuidos,
                "afinidade": self.afinidade,
                "limite_rituais": self.limite_de_rituais_para_aprender}

            requests.patch(f"{self.banco_dados}/personagens/{self.nome}/.json", data=json.dumps(dados))

# personagem = Personagem(nome)
# personagem.aumenta_nivel_de_exposicao()
