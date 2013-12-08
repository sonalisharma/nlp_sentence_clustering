$( document ).ready(function() {
  console.log("inside js");

$(".slideUpbox").click(function () {
  console.log("here");
   $(this).slideUp(2000);
});


  /* $(".question").click(function () {
    console.log($(this))
    $("#twitter .description").slideToggle("slow");
    $("#twitter .minimize").show();

}); */

  var someGlobalArray = new Array;

  $("input[type='checkbox']").click(function() {
    console.log("I am inside click");
      someGlobalArray=[];
      $('#category:checked').each(function() {
          someGlobalArray.push($(this).val());
      });
      console.log(someGlobalArray);
        var data = {
      data: JSON.stringify({
                        "value":someGlobalArray
                  })
   };
$.ajax({
   url:"/data",
   type: 'POST',
   data: data,
  success: function(msg){
              var myDiv = $('.answers'); // The place where you want to inser the template
              myDiv.html("");
              myDiv.html(msg);
            }
});
  });



  });
