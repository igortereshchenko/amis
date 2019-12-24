window.addEventListener("load", () => {

    checkPkInputDisplay();

    $('#is-null-checkbox').on("click", function () {
        checkPkInputDisplay();
    });

    function checkPkInputDisplay() {
        var pk_input =  $("#is-pk-input");
        if ($('#is-null-checkbox').is(':checked')){
            debugger;
             pk_input.prop( "checked", false );
             pk_input.prop( "disabled", true );
        }
        else {
             pk_input.prop( "disabled", false );
        }
    }
});