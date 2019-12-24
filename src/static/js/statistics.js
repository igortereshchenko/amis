window.addEventListener("load", (e) => {

    $('#classify-button').on("click", function () {
        var value = $("#classify-input").val();
        var payload = value.split(',');

        $.post("/classification", JSON.stringify(payload), function (data) {
            const container = $("#classification-table-body");
            container.html("");
            debugger;
            data.forEach((entity,) => {
                container.append($(`
                        <tr>
                            <td>${entity.name}</td>
                            <td>${entity.value}</td>
                        </tr>`))
            });
        }, "json");
    });
});