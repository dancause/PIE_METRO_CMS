function modify_user(id){


            var xhr = new XMLHttpRequest();
            var add_comment = document.getElementById('usager_'+id);
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
                "id": id,
                "nom": document.getElementById('nom_'+id).value,
                "courriel": document.getElementById('courriel_'+id).value,
                "role": document.getElementById('role_'+id).value,
                "actif": document.getElementById('actif_'+id).checked,
                "picture": document.getElementById('picture_'+id).value,
            };

            xhr.open('POST', '/gestion/user/update', true);
            xhr.setRequestHeader("Content-Type", "application/json");
            xhr.send(JSON.stringify(datajson));

}



function forget_password() {
      var xhr = new XMLHttpRequest();
            var login = document.getElementById('reset_password');
            xhr.onreadystatechange = function() {
              if (xhr.readyState === XMLHttpRequest.DONE)
              {
                      if (xhr.status === 200)
                      {
                      login.innerHTML = xhr.responseText;
                      }
                      else
                      {
                      login.innerHTML = ('Erreur avec le serveur / Server Error');
                      }
              }
            };

            xhr.open('GET', '/login/change/password', true);
            xhr.send();


}

