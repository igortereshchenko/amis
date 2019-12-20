$(function(){
	$('button').click(function(){
		var faculty = $('#faculty').val();
		$.ajax({
			url: '/try',
			data: $('form').serialize(),
			type: 'POST',
			success: function(response){
				console.log(response);
			},
			error: function(error){
				console.log(error);
			}
		});
	});
});