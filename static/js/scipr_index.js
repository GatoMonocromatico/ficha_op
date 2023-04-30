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
const pv_modificar = $("#dano_pv")
const pe_modificar = $("#dano_pe")
const sn_modificar = $("#dano_sn")
const personagem = $("h1").text().replace("Ficha ", "").toLowerCase()
const pericias = $("#text_pericias")
const rituais = $("#text_rituais")
const poderes = $("#text_poderes")
const inventario = $("#text_inventario")
const anotacoes = $("#text_anotacoes")
const infos = $("#text_infos")
const divDesc = $("#text_desc")
var pvModificar = 0
var peModificar = 0
var snModificar = 0
var nomeRituais = []
var nomePoderes = []

function setaVariaveisParaRequestPte(acao) {
    var pvModificar = pv_modificar.val()
    var peModificar = pe_modificar.val()
    var snModificar = sn_modificar.val()

    dados = { "personagem": personagem, "pv": pvModificar, "pe": peModificar, "sn": snModificar, "ação": acao}
    console.log(dados)
}

document.addEventListener("DOMContentLoaded", function () {
    $("#escurecer_tela").css("visibility", "visible")
    $("#bloco_carregador_de_tela").css("visibility", "visible")

    $.ajax({
        url: `https://apiordemparanormal.onrender.com/receber-formatado/${personagem}`,
        type: "GET",
        success: function (result) {
            let r_agi = result["atributos"]["agi"]
            let r_forca = result["atributos"]["for"]
            let r_int = result["atributos"]["int"]
            let r_pre = result["atributos"]["pre"]
            let r_vig = result["atributos"]["vig"]
            let r_nex = result["nex"]
            let r_defesa = result["defesa"]
            let r_pv = result['pv']
            let r_pe = result['pe']
            let r_sn = result['sn']
            let r_pericias = result["pericias"]
            let r_rituais = result["rituais"]
            let r_poderes = result["poderes"]
            let r_inventario = result["inventario"]
            let r_anotacoes = result["anotações"]
            let r_trilha = result["trilha"]
            let r_afinidade = result["afinidade"]
            let r_origem = result["origem"]
            let r_classe = result["classe"]

            agi.text(r_agi)
            forca.text(r_forca)
            int.text(r_int)
            pre.text(r_pre)
            vig.text(r_vig)
            nex.text(r_nex)
            defesa.text(r_defesa)
            pv.text(r_pv)
            pe.text(r_pe)
            sn.text(r_sn)
            pericias.text(r_pericias)
            anotacoes.text(r_anotacoes)
            inventario.text(r_inventario)

            infos.text(`Afinidade\n${r_afinidade}\n\nClasse\n${r_classe}\n\nOrigem\n${r_origem}\n\nTrilha\n${r_trilha}`)
            
            poderes.text("")
            if (r_rituais != "Nenhum") {
                rituais.text("")

                for (let ritual in r_rituais){
                    let id = ritual.replace(" ", "_")

                    nomeRituais.push(id)

                    let label = $(`<label id="${id}" class="label_habilidades">${r_rituais[ritual].replace("\n", "<br>")}</label>`)

                    rituais.append(label)
                    rituais.append($("<br>"))
                    rituais.append($("<br>"))

                    let elemento = document.getElementById(id)

                    elemento.addEventListener("click", function() {
                        $.ajax({
                            url: "https://apiordemparanormal.onrender.com/receber/info",
                            contentType: "application/json",
                            type: "POST",
                            data: JSON.stringify({"tipo": "rituais", "habilidade": id}),
                            success: function(result) {
                                if (result === "") {
                                    resultado = "Não temos a descrição desta habilidade ainda"
                                } else {
                                    resultado = result
                                }
                                $("#descricao").css("visibility", "visible")
                                divDesc.text(resultado)
                            },
                            error: function (e) {
                                console.log(e)
                                console.log(JSON.stringify({"tipo": "poderes", "habilidade": id}))
                            }
                        })
                    })
                }
            }else {
                rituais.text(r_rituais)
            }
            for (let poder in r_poderes){
                let id = poder.replace(" ", "_")

                nomePoderes.push(id)

                let label = $(`<label id="${id}" class="label_habilidades">${r_poderes[poder].replace("\n", "<br>")}</label>`)

                poderes.append(label)
                poderes.append($("<br>"))
                poderes.append($("<br>"))

                let elemento = document.getElementById(id)

                elemento.addEventListener("click", function() {
                    $.ajax({
                        url: "https://apiordemparanormal.onrender.com/receber/info",
                        contentType: "application/json",
                        type: "POST",
                        data: JSON.stringify({"tipo": "poderes", "habilidade": id}),
                        success: function(result) {
                            if (result === "") {
                                resultado = "Não temos a descrição desta habilidade ainda"
                            } else {
                                resultado = result
                            }
                            $("#descricao").css("visibility", "visible")
                            divDesc.text(resultado)
                        },
                        error: function (e) {
                            console.log(e)
                            console.log(JSON.stringify({"tipo": "poderes", "habilidade": id}))
                        }
                    })
                })
            }

            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
    })
})

$("#btn_pte_soma").click(function () {
    setaVariaveisParaRequestPte("cura")

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
        },
        success: function (result) {
            let r_pv = result['pv']
            let r_pe = result['pe']
            let r_sn = result['sn']

            pv.text(r_pv)
            pe.text(r_pe)
            sn.text(r_sn)

            pv_modificar.val("")
            pe_modificar.val("")
            sn_modificar.val("")

            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
    })
})

$("#btn_pte_subtrai").click(function () {
    setaVariaveisParaRequestPte("dano")

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
        },
        success: function (result) {
            console.log(result)

            let r_pv = result['pv']
            let r_pe = result['pe']
            let r_sn = result['sn']

            pv.text(r_pv)
            pe.text(r_pe)
            sn.text(r_sn)

            pv_modificar.val("")
            pe_modificar.val("")
            sn_modificar.val("")

            $("#escurecer_tela").css("visibility", "hidden")
            $("#bloco_carregador_de_tela").css("visibility", "hidden")
        }
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

$("#xdesc").on("click", function() {
    $("#descricao").css("visibility", "hidden")
})
