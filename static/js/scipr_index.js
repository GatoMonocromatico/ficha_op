const agi = $("#agi")
const forca = $("#for")
const int = $("#int")
const pre = $("#pre")
const vig = $("#vig")
const nex = $("#nex")
const defesa = $("#defesa")
const pv = $("#pv_val")
const pe = $("#pe_val")
const sn = $("#sn_val")
const personagem = $("h1").text().replace("Ficha ", "").toLowerCase()
const pericias = $("#text_pericias")
const rituais = $("#text_rituais")
const poderes = $("#text_poderes")
const inventario = $("#text_inventario")
const anotacoes = $("#text_anotacoes")
var pvModificar = 0
var peModificar = 0
var snModificar = 0

function setaVariaveisParaRequestPte(acao) {
    var pvModificar = pv.val()
    var peModificar = pe.val()
    var snModificar = sn.val()

    if (pvModificar == "") {
        pvModificar = 0
    }
    if (peModificar == "") {
        peModificar = 0
    }
    if (snModificar == "") {
        snModificar = 0
    }

    pvModificar = parseInt(pvModificar)
    peModificar = parseInt(peModificar)
    snModificar = parseInt(snModificar)

    if (acao != "subtrair") {
        pvModificar = pvModificar * -1
        peModificar = peModificar * -1
        snModificar = snModificar * -1
    }

    dados = { "personagem": personagem, "pv": pvModificar, "pe": peModificar, "sn": snModificar }
    console.log(dados)
}

document.addEventListener("DOMContentLoaded", function () {
    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    $.ajax({
        url: `https://apiordemparanormal.onrender.com/receber/${personagem}`,
        type: "GET",
        success: function (result) {
            console.log("carregou")
            let r_agi = result["atributos"]["agi"]
            let r_forca = result["atributos"]["for"]
            let r_int = result["atributos"]["int"]
            let r_pre = result["atributos"]["pre"]
            let r_vig = result["atributos"]["vig"]
            let r_nex = result["nex"].toString()
            let r_defesa = result["defesa"]
            let r_pv_atual = result['pv']['atual'].toString()
            let r_pe_atual = result['pe']['atual'].toString()
            let r_sn_atual = result['sn']['atual'].toString()
            let r_pv_max = result['pv']['maximo'].toString()
            let r_pe_max = result['pe']['maximo'].toString()
            let r_sn_max = result['sn']['maximo'].toString()
            let r_pericias = result["pericias"]
            let r_rituais = result["rituais"]
            let r_poderes = result["poderes"]
            let r_inventario = result["inventario"]
            let r_anotacoes = result["anotações"]  
            
            let pericias_dict = {}

            let pericias_formatado = pericias.text()
            let rituais_formatado = ""
            let poderes_formatado = ""
            let inventario_formatado = ""
            
            let pericia;
            let linha_pericias_text;
            let letra_pericia;
            let ritual;
            let poder;
            let item;

            let len_maior_pericia = 16

            if (r_pericias["sobrevivência"] != undefined && r_pericias["sobrevivência"] != "t") {
                len_maior_pericia += 1
            }

            let numero_de_casas_numericas_dos_pte = {"atuais": [], "maximos": []}
            let dict_listas_pte = { "atuais": [r_pv_atual, r_pe_atual, r_sn_atual], "maximos": [r_pv_max, r_pe_max, r_sn_max] }

            let list_val_len_pte = []

            let lista_pericias = pericias.text().split("\n")

            if (r_nex.length == 1) {
                r_nex = `0${r_nex}%`
            }

            for (let index = 0; index < 2; index++) {
                list_val_len_pte = []

                if (index == 0) {
                    indent_lista = "atuais"
                }
                else {
                    indent_lista = "maximos"
                }

                numero_de_casas_numericas_dos_pte[indent_lista] = Math.max(...dict_listas_pte[indent_lista]).toString().split("").length

            }

            let r_pv_atual_formatado = r_pv_atual
            let r_pe_atual_formatado = r_pe_atual
            let r_sn_atual_formatado = r_sn_atual

            let r_pv_maximos_formatado = r_pv_max
            let r_pe_maximos_formatado = r_pe_max
            let r_sn_maximos_formatado = r_sn_max

            for (let i = 0; i < numero_de_casas_numericas_dos_pte["atuais"]; i++) {
                if (r_pv_atual_formatado.length < numero_de_casas_numericas_dos_pte["atuais"]) {
                    r_pv_atual_formatado = "0" + r_pv_atual_formatado
                }
                if (r_pe_atual_formatado.length < numero_de_casas_numericas_dos_pte["atuais"]) {
                    r_pe_atual_formatado = "0" + r_pe_atual_formatado
                }
                if (r_sn_atual_formatado.length < numero_de_casas_numericas_dos_pte["atuais"]) {
                    r_sn_atual_formatado = "0" + r_sn_atual_formatado
                }
            }

            for (let i = 0; i < numero_de_casas_numericas_dos_pte["maximos"]; i++) {
                if (r_pv_maximos_formatado.length < numero_de_casas_numericas_dos_pte["maximos"]) {
                    r_pv_maximos_formatado = "0" + r_pv_maximos_formatado
                }
                if (r_pe_maximos_formatado.length < numero_de_casas_numericas_dos_pte["maximos"]) {
                    r_pe_maximos_formatado = "0" + r_pe_maximos_formatado
                }
                if (r_sn_maximos_formatado.length < numero_de_casas_numericas_dos_pte["maximos"]) {
                    r_sn_maximos_formatado = "0" + r_sn_maximos_formatado
                }
            }

            let nivel_treinamento = ""

            for (pericia in r_pericias) {
                nivel_treinamento = r_pericias[pericia]

                if (nivel_treinamento == "t") {
                    nivel_treinamento = 5
                }
                else if (nivel_treinamento == "v") {
                    nivel_treinamento = 10
                }
                else {
                    nivel_treinamento = 15
                }

                pericias_dict[pericia] = nivel_treinamento
            }

            for (ritual in r_rituais) {
                let circulo = parseInt(r_rituais[ritual])

                if (circulo == 1) {
                    circulo = "1º círculo"
                }
                else if (circulo == 2) {
                    circulo = "2º círculo"
                }
                else if (circulo == 3) {
                    circulo = "3º círculo"
                }
                else {
                    circulo = "4º círculo"
                }

                rituais_formatado = `${rituais_formatado}${ritual}\n(${circulo})\n\n`
            }

            if (rituais_formatado == "") {
                rituais_formatado = "Nenhum"
            }
            
            for (poder in r_poderes) {
                let custo = parseInt(r_poderes[poder])

                if (custo == 0) {
                    custo = "condição"
                }
                else {
                    custo = custo + " PE"
                }

                poderes_formatado = `${poderes_formatado}${poder}\n(${custo})\n\n`
            }

            agi.text(r_agi)
            forca.text(r_forca)
            int.text(r_int)
            pre.text(r_pre)
            vig.text(r_vig)
            nex.text(`Nex: ${r_nex}`)
            defesa.text(`Defesa: ${r_defesa}`)
            pv.text(`PV: ${r_pv_maximos_formatado}/${r_pv_atual_formatado}`)
            pe.text(`PE: ${r_pe_maximos_formatado}/${r_pe_atual_formatado}`)
            sn.text(`SN: ${r_sn_maximos_formatado}/${r_sn_atual_formatado}`)
            
            for (linha_pericias_text in lista_pericias) {
                linha_pericias_text = lista_pericias[linha_pericias_text]

                let nivel_treinamento = linha_pericias_text.substring(linha_pericias_text.length - 2).replace("+", "")
                let pericia = linha_pericias_text.replace(` +${nivel_treinamento}`, "")

                if (pericias_dict[pericia] == undefined) {
                    pericias_dict[pericia] = 0
                }

                let linha_reformatada = linha_pericias_text.replace(nivel_treinamento, pericias_dict[pericia])

                while (linha_reformatada.length < len_maior_pericia) {
                    linha_reformatada = linha_reformatada.replace(" ", "  ")
                }

                pericias_formatado = pericias_formatado.replace(linha_pericias_text, linha_reformatada)
            }

            pericias.text(pericias_formatado)
            rituais.text(rituais_formatado)
            poderes.text(poderes_formatado)

            for (item in r_inventario) {
                let carga = parseInt(r_inventario[item])
                let categoria = r_inventario[item].replace(`${carga} `, "")

                inventario_formatado += `${item}\n(Carga: ${carga}|Categoria: ${categoria})\n\n`
            }

            anotacoes.text(r_anotacoes)
            inventario.text(inventario_formatado)

            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
    })
})

$("#btn_pte_soma").click(function () {
    setaVariaveisParaRequestPte("adicionar")

    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    $.ajax({
        url: "https://apiordemparanormal.onrender.com/alterar/pte",
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(dados),
        error: function (e) {
            console.log(e)
        }
    }).done(function (data) {

        let respPv = data["pv"].toString()
        let respPe = data["pe"].toString()
        let respSn = data["sn"].toString()

        let listaLenPte = [respPv.length, respPe.length, respSn.length]
        let maiorLen = Math.max(...listaLenPte)



        for (let i = 0; i < maiorLen; i++) {
            if (respPv.length < maiorLen) {
                respPv = "0" + respPv
            }
            if (respPe.length < maiorLen) {
                respPe = "0" + respPe
            }
            if (respSn.length < maiorLen) {
                respSn = "0" + respSn
            }
        }

        pv.text(`${pv.text().split("/")[0]}/${respPv}`)
        pe.text(`${pe.text().split("/")[0]}/${respPe}`)
        sn.text(`${sn.text().split("/")[0]}/${respSn}`)

        $("#dano_pv").val("")
        $("#dano_pe").val("")
        $("#dano_sn").val("")

        $("#escurecer_tela").css("visibility", "hidden")
        $("#bloco_carregador_de_tela").css("visibility", "hidden")
    })

})
$("#btn_pte_subtrai").click(function () {
    setaVariaveisParaRequestPte("subtrair")

    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    $.ajax({
        url: "https://apiordemparanormal.onrender.com/alterar/pte",
        type: "POST",
        dataType: "json",
        contentType: "application/json",
        data: JSON.stringify(dados),
        error: function (e) {
            console.log(e)
        }
    }).done(function (data) {

        let respPv = data["pv"].toString()
        let respPe = data["pe"].toString()
        let respSn = data["sn"].toString()

        let listaLenPte = [respPv.length, respPe.length, respSn.length]
        let maiorLen = Math.max(...listaLenPte)



        for (let i = 0; i < maiorLen; i++) {
            if (respPv.length < maiorLen) {
                respPv = "0" + respPv
            }
            if (respPe.length < maiorLen) {
                respPe = "0" + respPe
            }
            if (respSn.length < maiorLen) {
                respSn = "0" + respSn
            }
        }

        pv.text(`${pv.text().split("/")[0]}/${respPv}`)
        pe.text(`${pe.text().split("/")[0]}/${respPe}`)
        sn.text(`${sn.text().split("/")[0]}/${respSn}`)

        $("#dano_pv").val("")
        $("#dano_pe").val("")
        $("#dano_sn").val("")

        $("#escurecer_tela").css("visibility", "hidden")
        $("#bloco_carregador_de_tela").css("visibility", "hidden")
    })

})

$("#btn_anotacoes").click(function() {
    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    let anotacoes_salvar = anotacoes.val()
    let dados = {"anotações": anotacoes_salvar, "personagem": personagem}

    console.log(dados)

    $.ajax({
        url: "https://apiordemparanormal.onrender.com/alterar/anotacoes",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify(dados),
        error: function (e) {
            console.log(e)
        },
        success: function () {
            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
    })
    
})

$("#btn_atualiza_inv").click(function() {
    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    $.ajax({
        url: `https://apiordemparanormal.onrender.com/receber/${personagem}`,
        type: "GET",
        success: function (result) {
            let r_inv = result["inventario"]
            let inventario_formatado = ""
            let item;

            for (item in r_inv) {
                let carga = parseInt(r_inv[item])
                let categoria = r_inv[item].replace(`${carga} `, "")

                inventario_formatado += `${item}\n(Carga: ${carga}|Categoria: ${categoria})\n\n`
            }

            inventario.text(inventario_formatado)

            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
    })
})
