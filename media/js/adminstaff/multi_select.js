function idArray(){
	var idArray = Array();
	
	$("input[name='checkop']:checkbox").each( function(){  
alert($(this).attr('checked'));
			if ($(this).attr("checked")){
				idArray.push($(this).val())
				alert($(this).val());  	
			}
		}
	)   
	return idArray;
}

function selectThis(){
	var selectedArray = new Array();
	selectedArray = idArray();
	var selectedString = selectedArray.join(',');
	//alert(selectedString);
}
