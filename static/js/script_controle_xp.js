const divPersonagens = $("#div_personagens")

$("#carregamento_fundo").css("visibility", "visible")
$("#carregando").css("visibility", "visible")
$.ajax({
    url: "https://apiordemparanormal.onrender.com/receber/nomes",
    type: "GET",
    contentType: "application/json",
    success: function(result) {        
        let nome;
        for (nome in result) {

            let nomeId = nome.replace(" ", "_")

            let container = $(`<label id='${nomeId}_label' class='container'></label>`)
            let inputCheckbox = $(`<input id='${nomeId}_inp' type='checkbox' class='inp_check' value='${nomeId}' name='${nomeId}'>`)
            let spanCheckbox = $(`<span id='${nomeId}_span' class='checkmark'></span>`)
            let labelNome = $(`<label id='${nomeId}_nome'> ${nome[0].toUpperCase() + nome.substring(1)}</label>`)
            let spanStatus = $(`<span id='${nomeId}_span_status' class='span_status'></span>`)

            divPersonagens.append(container)

            let esteContainer = $(`#${nomeId}_label`)
            
            esteContainer.append(inputCheckbox)
            esteContainer.append(spanCheckbox)
            esteContainer.append(labelNome)
            
            let esteLabelNome = $(`#${nomeId}_nome`)

            esteLabelNome.append(spanStatus)
            

            if (result[nome] == true) {
                $(`#${nomeId}_span_status`).css("background-color", "green")
            }
            else {
                $(`#${nomeId}_span_status`).css("background-color", "red")
            }

            $("#carregamento_fundo").css("visibility", "hidden")
            $("#carregando").css("visibility", "hidden")
        }
    }
})