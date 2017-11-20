function sauvegarde(){

var Auteur = document.getElementById("auteur").value;
var datepub = document.getElementById("datepublication").value;
var titre_fr = document.getElementById("titre_fr").value;
var titre_ang = document.getElementById("titre_ang").value;
var testefr = CKEDITOR.instances.editor_fr.getData(),
var texteang = CKEDITOR.instances.editor_ang.getData(),
var url = document.getElementById("URL").value,
var categories = document.getElementById("categorie").value,
var tagang = document.getElementById("tag").value,
var tagfr = document.getElementById("etiquettes").value,
var photo = document.getElementById("photo").value

console.log(Auteur+"  "+datepub);

var datajson={
	"texte_fr": CKEDITOR.instances.editor_fr.getData(),
	"texte_ang": CKEDITOR.instances.editor_ang.getData(),
	"titre_fr": document.getElementById("titre_fr").value,
	"titre_eng": document.getElementById("titre_ang").value,
	"url": document.getElementById("URL").value,
	"auteur": document.getElementById("auteur").value,
	"categorie": document.getElementById("categorie").value,
	"tag": document.getElementById("tag").value,
	"etiquettes": document.getElementById("etiquettes").value,
	"datepub": document.getElementById("datepublication").value,
	"photo_1": document.getElementById("photo").value
	};	
	console.log(datajson);	
	$.ajax({
            url: '/test',
            data: JSON.stringify(datajson),
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            success: '/create_article'
            });         
};


        