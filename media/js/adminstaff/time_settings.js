function time_settings(){
	$("#time_settings_error_message").empty();
	Dajaxice.adminStaff.DeadlineSettings(time_settings_callback,{'form':$('#time_settings_form').serialize(true)});
	}
function time_settings_callback(data){
	if (data.status == "1"){
		// if success all field background turn into white
		$.each(data.field,function(i,item){
				object = $('#'+item);
				object.css("background","white");
				});
		//$("#time_settings_form").css("background","white");
		$("#time_settings_error_message").append("<strong>"+data.message+"</strong>")
		}
	else
		{
			$.each(data.field,function(i,item){
				object = $('#'+item);
				object.css("background","white");
				});
			//error field background turn into red
			$.each(data.error_id,function(i,item){
				object = $('#'+item);
				object.css("background","red");
				});
			$("#time_settings_error_message").append("<strong>"+data.message+"</strong>")
		}
	}