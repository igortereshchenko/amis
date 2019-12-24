$( "#update" ).click(function( event ) {
  const form = $('#form');
  $.ajax({
    type: 'put',
    data: form.serialize(),
    success: function(result) {
        window.location.replace("/groups/");
    },
    error: function (err) {
      alert(err.responseText);
    }
  });
});


function deleteGroup(id) {
  $.ajax({
    type: 'delete',
    success: function(result) {
        window.location.replace("/groups/");
    },
    error: function (err) {
      alert(err.responseText);
    }
  });
}