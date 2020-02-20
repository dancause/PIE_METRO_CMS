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
        photo_list = photo_list + id_photo + ',';
    }
    return photo_list;
}


function removephotolist(photo_list , id_photo){

var res = photo_list.replace(id_photo+',', "");
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

    var a = verif_cookie().split(",");
    var colonne = radiocheck('colonne');
    var style = radiocheck('style');
    var grid = document.getElementById('grid').value;
    var moreStyle = document.getElementById('moreStyle').value;
    var compteur=1;
    var cols = 12 / colonne;
    var j=0;

    console.log(a.length);
    var tempgall = "";
    var gallery = '<div class="row text-center">';

    for (i in a) {
        if (a[i] != "") {
                    gallery = gallery +'<div class=" gallery_ligne col-'+grid + cols + '"><a href="/view/' + a[i]+'"><img class="img-fluid ' + style + '" src="/images/' + a[i] + '" alt="' + a[i] + '" style="'+moreStyle+'" ></a></div>';
                            if(compteur < colonne){

                                compteur++;
                            } else{
                                gallery = gallery +'</div><div class="row text-center">';
                                compteur=1;
                            }
        }
    }
    gallery=gallery+'</div>';

document.getElementById("gallery_html").value = gallery;
}

function radiocheck(rname) {
    return document.querySelector('input[name='+rname +']:checked').value;
}


function photoentete(id_photo,index){

 var element = document.getElementsByName("header_photo");
    for (var i = 0; i<element.length; i++) {
        if (element[i].style.visibility == "visible") {

            element[i].style.visibility = "hidden";
        }

    }
document.getElementById("photo").value = id_photo;
document.getElementById("entete_"+index).style.visibility = "visible";
console.log(document.getElementById("entete_"+index).style.visibility );

}
