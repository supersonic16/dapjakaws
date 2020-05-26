/* jquery code */
$(document).ready(function(){

  if ($(window).width() < 992){
    $("#navbrand").removeClass("pl-2");
    $("#myForm").addClass("w-100");

  }
  else if (searchText.value == false){
    $("#searchText").hide();
  }
  else{
      $("#searchText").show();
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
    }
  });
  $(window).resize(function(){
      if ($(window).width() < 992){
        $("#mydiv").removeClass("input-group flex-box");
        $("#navbrand").removeClass("pl-2");
        $("#myForm").addClass("w-100");
      }
      else{
        $("#mydiv").addClass("input-group flex-box");
        $("#navbrand").addClass("pl-2");
        $("#myForm").removeClass("w-100");
      }
  });

  $("#collapseButton").click(function(){
      $("#searchText").show();
      $("nav").removeClass("fixed-top");
      $("#topNav").addClass("scrollTop");
  });


$("#id_title").attr("placeholder", "Title");
$("#id_sub_title").attr("placeholder", "Sub title");
$("#id_credit").attr("placeholder", "Image credits");
$("#id_content").attr("placeholder", "Write your story");


});
