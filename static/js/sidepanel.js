 $(document).ready(function(){

var xhr = new XMLHttpRequest();
xhr.onreadystatechange = function() {
	if (xhr.readyState === XMLHttpRequest.DONE) 
	{
        	if (xhr.status === 200) 
        	{
        	sidepanel.innerHTML = xhr.responseText;
        	} 
        	else
        	{
        	console.log('Erreur avec le serveur');
        	}
	}  
};
xhr.open("GET", '/sidepanel', true);
xhr.send();  	
})
