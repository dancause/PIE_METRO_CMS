function verif_cookie(){
    var photo_list='';
        photo_list = getCookie('List_photo');
         if (photo_list ==''){
             setCookie('List_photo','');
         }
    return photo_list;
}


function build_list(id_photo,index){

    var PHOTO = document.getElementById('photo_'+index);
    var liste = verif_cookie();

    if (PHOTO.style.backgroundColor == "lightgrey") {
            PHOTO.style.backgroundColor = "";
            var res = removephotolist(liste,id_photo);
            setCookie('List_photo',res);
        } else {
            PHOTO.style.backgroundColor='lightgrey';
            liste = validlist(liste, id_photo);
            setCookie('List_photo',liste);
        }
}


function validlist( photo_list , id_photo){
    if ( photo_list.indexOf(id_photo) == -1){
        photo_list = photo_list + id_photo + ', ';
    }
    return photo_list;
}


function removephotolist(photo_list , id_photo){

var res = photo_list.replace(id_photo, "");
return res;
}
window.onload = function(){
    deleteCoookie('List_photo');
};

function reset() {
    deleteCoookie('List_photo');
    document.getElementById("gallery_html").value="";
    console.log(document.getElementsByName("photo_gallery"));

    var element = document.getElementsByName("photo_gallery");


    for (var i = 0; i<element.length; i++) {
        if (element[i].style.backgroundColor == "lightgrey") {

            element[i].style.backgroundColor = "";
        }

    }

}


function create(){

    var a = verif_cookie().split(", ");

    for (i in a) {
   console.log( a[i]);
}

}