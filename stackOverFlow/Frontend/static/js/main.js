$( document ).ready(function() {
  console.log("I am here");
	var selected_cat =[];
  	$( ".checkbox" ).click(function() {
  		alert($('#categories').val());
  		$('input[name="checkbox"]:checked').each(function() {
   			selected_cat.push((this.value)); 
			});

		alert(selected_cat);

  		

     	var request = $.ajax({
         type: "POST",
         url: "data",
         data: {'input_value':$('#categories').val()},
         dataType: "html"
         }).done(function(msg) {
              // I don't know what you want to do with a return value...
              // or if you even want a return value
  }
)

    });

  });