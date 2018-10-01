function build_list(id_photo,index){
var photo_list;
photo_list = getCookie('List_photo');
 if (photo_list ==''){
     setCookie('List_photo',id_photo);
 }
var listvalider = validlist(photo_list,id_photo);
 setCookie('List_photo',listvalider);

}


function alert_photo(index){
    var PHOTO = document.getElementById(index);
    if (PHOTO.style.backgroundColor === "lightgrey") {
            PHOTO.style.backgroundColor = "";
            removephotolist();
        } else {
            PHOTO.style.backgroundColor='lightgrey';
            validlist()
        }
}


function validlist( photo_list , id_photo){
    if ( photo_list.indexOf(id_photo) == -1){
        photo_list = photo_list + ', '+id_photo;
    }
    return photo_list;
}


function removephotolist(photo_list , id_photo){

}
window.onload = function(){
    deleteCoookie('List_photo');
};