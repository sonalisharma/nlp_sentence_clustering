$( document ).ready(function() {
  console.log("inside js");

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
              var myDiv = $('#answers'); // The place where you want to inser the template
              myDiv.html(msg);
            }
});
  });


  /*$('#category').click(function () {
    console.log("Categories changed");
            if ($('#category').is(':checked')) {
                $.ajax({
                    url: '/data',
                    data: { isLocked: "Something" },
                    type: 'POST',
                    dataType: "json"
                });
            }
}); */

  });
/*

function handleclick(cb){

  var data = {
      data: JSON.stringify({
                        "value":$("input[type='checkbox']").val()
                  })
   };
$.ajax({
   url:"/data",
   type: 'POST',
   data: data,
   success: function(msg){
              alert(msg);
            }
}); */