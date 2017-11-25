function Add_Comments() { 
if(document.getElementById('comment').value != ""){
            var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('add_comment');
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE) 
              {
                      if (xhr.status === 200) 
                      {  
                      add_comment.innerHTML = xhr.responseText;
                      } 
                      else
                      {
                      add_comment.innerHTML = ('Erreur avec le serveur / Server Error');
                      }
              }  
            };
            var datajson={
              "id_article": document.getElementById('id_article').value,
              "comment": document.getElementById('comment').value
            };
            vider_comments();
            xhr.open('POST', '/comments', true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify(datajson));
  } else {

    console.log("commentaire vide");
  }
}

function vider_comments(){

document.getElementById('comment').value = "";

}

