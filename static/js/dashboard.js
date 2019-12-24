window.addEventListener("load", (e) => {

     $('#entity_attributes_population_select').on("change", function () {
         var value = $(this).find("option:selected").val();
         $.getJSON(`/entity_attributes_population/${value}`, data => {
            Plotly.newPlot('entity_attributes_population_graph', data, {});
        })
     });
});