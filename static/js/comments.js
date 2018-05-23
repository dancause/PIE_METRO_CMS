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


function hidden(index_comment){
    var TR_LIGNE = document.getElementById(index_comment);
    if (TR_LIGNE.style.display === "none") {
            TR_LIGNE.style.display = "block";
        } else {
            TR_LIGNE.style.display = "none";
        }
}

function alert_comment(index_comment){
    var TR_LIGNE = document.getElementById(index_comment);
    if (TR_LIGNE.style.backgroundColor === "red") {
            TR_LIGNE.style.backgroundColor = "";
            document.getElementById("checkbox_validate_"+index_comment).disabled = false;
        } else {
            TR_LIGNE.style.backgroundColor='red';
            document.getElementById("checkbox_validate_"+index_comment).disabled = true;
        }

}

function validat_comment( index_comment){
    var TR_LIGNE = document.getElementById(index_comment);
    var xhr = new XMLHttpRequest();
    console.log('état de la case check  '+document.getElementById("checkbox_validate_"+index_comment).checked)
    if(document.getElementById("checkbox_validate_"+index_comment).checked === true){
           hidden(index_comment);
            xhr.open('POST', '/valider/comments/'+index_comment, true);
             //console.log('check')
            xhr.send();
    }else if (document.getElementById("checkbox_validate_"+index_comment).checked === false) {
            xhr.open('POST', '/unvalider/comments/'+index_comment, true);
            //console.log('uncheck')
            xhr.send();
    }

}

function signal_comment( index_comment){
    var TR_LIGNE = document.getElementById(index_comment);
    alert_comment(index_comment);
    var xhr = new XMLHttpRequest();
            xhr.open('POST', '/valider/signaler/comments/'+index_comment, true);
            xhr.send();
}

function comments_valided(){
    console.log("comment signal");
            var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('liste_comments');
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
            xhr.open('GET', '/validated/comments', true);
            xhr.send();

}

function comments_signaled(){
  console.log("comment signal");
   var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('liste_comments');
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
            xhr.open('GET', '/signaled/comments', true);
            xhr.send();
}

function all_comments(){
  console.log("comment signal");
   var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('liste_comments');
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
            xhr.open('GET', '/all/comments', true);
            xhr.send();
}

function comments_unvalided(){
  console.log("comment signal");
   var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('liste_comments');
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
            xhr.open('GET', '/unvalidated/comments', true);
            xhr.send();
}