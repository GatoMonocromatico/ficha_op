const inp = $("#inp")

inp.on("keydown", function(event) {
    if (event.key === "Enter") {
        $("btn").click()
    }
})