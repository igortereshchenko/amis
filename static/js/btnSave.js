$("#btnSave").click(function () {


    $.ajax({
    type:"GET",
    url:"try",
    data:{
        'message':$("#txtMessage").val()
    },
    dataType:"text",
    cache:false,
    success:function (data) {
        alert(data)
        return true
    }
    });

});