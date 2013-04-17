function getOs() 
{ 
	var checkerror=false;
	if(isSafari=navigator.userAgent.indexOf("Safari")>0) { 
        checkerror=true;
	} 
    if(isFirefox=navigator.userAgent.indexOf("Firefox")>0){  
        checkerror=true;
    } 
    if(window.opera){  
        checkerror=true;
    } 
	if (checkerror==false) {
		$('#myModal').modal('show');
	};			
} 
window.onload = getOs;