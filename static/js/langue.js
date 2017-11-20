
function Changer_Langue(){
	if(document.getElementById('button_langue').value=='Français'){
			console.log(getCookie('langue'));
			setCookie('langue','FR');
			window.location = getURL();
	}else if(document.getElementById('button_langue').value=='Anglais'){
	    	console.log(getCookie('langue'));
			setCookie('langue','ENG');
			window.location = getURL(); 
			}		
}

function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i <ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}


function deleteCoookie(cname) {
    createCookie(cname,"",-1);
}


function setCookie(cname, value) {
    var cvalue = escape(value)
    document.cookie = cname + "=" + cvalue + "; path=/";
}

function getURL()
{
return document.location.pathname;

}