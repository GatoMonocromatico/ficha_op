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
var pvModificar = 0
var peModificar = 0
var snModificar = 0

function setaVariaveisParaRequestPte(acao) {
    var pvModificar = pv_modificar.val()
    var peModificar = pe_modificar.val()
    var snModificar = sn_modificar.val()

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
        url: `https://apiordemparanormal.onrender.com/receber-formatado/${personagem}`,
        type: "GET",
        success: function (result) {
            console.log("sucesso")
            console.log("carregou")
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
            rituais.text(r_rituais)
            poderes.text(r_poderes)
            anotacoes.text(r_anotacoes)
            inventario.text(r_inventario)

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

            $("#dano_pv").val("")
            $("#dano_pe").val("")
            $("#dano_sn").val("")

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
            let r_pv = result['pv']
            let r_pe = result['pe']
            let r_sn = result['sn']

            pv.text(r_pv)
            pe.text(r_pe)
            sn.text(r_sn)

            $("#dano_pv").val("")
            $("#dano_pe").val("")
            $("#dano_sn").val("")

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
