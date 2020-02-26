function showSearch(){
  var searchText= document.getElementById("searchText")
  var searchButton= document.getElementById("searchButton")
  if (searchText.value){
    console.log("here");
  }
  else{

    searchText.style.display='none';
    console.log("hey");
  }
}
