$(document).ready(function(){
   $('#gist').hide().fadeIn(800);
   $('#gistTwo').hide().fadeIn(4000);


    function isNumber(n){
      return typeof(n) != "boolean" && !isNaN(n);
    }

    function SubmitFrm(){
      var space = document.getElementById("redir").value;
      console.log(space);
      if( isNumber(space)){
        window.location = "/upload/"+space;
        return false;
      }else{
        return false;
      }
    }

    function fileUpload(){
      var space = document.getElementById("reserve").value;
      console.log("SpaceReserve request :"+space);
      if( isNumber(space)){
        console.log("GOT AN INTEGER");
        return false;
      }else{
        console.log("this is a response");
        return false;
      }
    }

    $('#gist').click( function(){
        console.log("got response!");
        $.getJSON('/api/_find_number', {} , function(data){
          console.log(data);
          return false;
        });
    });

    $('#takenn').click( function(){
        $.getJSON('/api/_route_taken', {space:3} , function(data){
          console.log(data);
          return false;
        });
    });


});
