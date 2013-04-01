function send_email_to_expert(){
	$("#expert_email_error_message").empty();
	Dajaxice.adminStaff.ExpertDispatch(ExpertDispatch_callback,{'form':$('#expert_email_send_form').serialize(true)});
	}
function ExpertDispatch_callback(data){
	if (data.status == "1"){
		$("#expert_mailbox").css("background","white");
		$("#expert_email_error_message").append("<strong>"+data.message+"</strong>")
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
			$("#expert_email_error_message").append("<strong>"+data.message+"</strong>")
		}
	}


function send_email_to_school(){
	$("#school_email_error_message").empty();
	Dajaxice.adminStaff.SchoolDispatch(SchoolDispatch_callback,{'form':$('#school_email_send_form').serialize(true)});
	}
function SchoolDispatch_callback(data){
	if (data.status == "1"){
		$("#school_mailbox").css("background","white");
		$("#school_email_error_message").append("<strong>"+data.message+"</strong>")
		}
	else
		{
			id = data.id;
			object = $('#'+id)
			object.css("background","red");
			$("#school_email_error_message").append("<strong>"+data.message+"</strong>")
		}
	}