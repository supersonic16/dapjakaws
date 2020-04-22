function showSearch(){
  var searchText= document.getElementById("searchText")
  var searchButton= document.getElementById("searchButton")

}
function hidepost(n){
  console.log(n);
  var a = '#'+n;
  console.log(a);
  $("#hidebutton").submit(function(event){
    event.preventDefault();
  });
  $("a").hide();

}
/* jquery code */
$(document).ready(function(){
  if ($(window).width() < 768){
    $("#navbrand").removeClass("pl-2");
  }
  else{
    $("#searchText").hide();
  }
  $("#searchButton").click(function(){
    var searchText= document.getElementById("searchText");
    if (searchText.value == false){
      $("#searchText").toggle();
      $("#myForm").submit(function(event){
        event.preventDefault();

      });
    }
    else {
      $("#myForm").unbind('submit');
      $("#searchText").show();
      searchText.value = "";
    }
  });
  $(window).click(function(){

  })
  $(window).resize(function(){
      if ($(window).width() < 768){
        $("#mydiv").removeClass("input-group flex-box");
        $("#navbrand").removeClass("pl-2");
      }
      else{
        $("#mydiv").addClass("input-group flex-box");
        $("#navbrand").addClass("pl-2");
      }
  });

  $("#collapseButton").click(function(){
      $("#searchText").show();
      $("nav").removeClass("fixed-top");
      $("#topNav").addClass("scrollTop");
  });

});
