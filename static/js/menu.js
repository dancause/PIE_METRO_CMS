 $(document).ready(function(){

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState === XMLHttpRequest.DONE) 
	{
        	if (xhr.status === 200) 
        	{
        	menu_cat.innerHTML = xhr.responseText;
        	} 
        	else
        	{
        	console.log('Erreur avec le serveur');
        	}
	}  
};
xhr.open("GET", '/menu_cat', true);
xhr.send();  	
})


