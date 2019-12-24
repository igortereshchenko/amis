$( "#update" ).click(function( event ) {
  const form = $('#form');
  $.ajax({
    type: 'put',
    data: form.serialize(),
    success: function(result) {
        window.location.replace("/lectures/");
    },
    error: function (err) {
      alert(err.responseText);
    }
  });
});


function deleteUser(id) {
  $.ajax({
    type: 'delete',
    success: function(result) {
        window.location.replace("/lectures/");
    },
    error: function (err) {
      alert(err.responseText);
    }
  });
}