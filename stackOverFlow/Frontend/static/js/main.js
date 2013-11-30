$( document ).ready(function() {
	console.log("I am here");
  
$('#categories').click(function() {
	alert("I am here");
        var data = { isChecked : $(this).is(':checked') };
        console.log(data);
        $.post('/', data);

    });


});