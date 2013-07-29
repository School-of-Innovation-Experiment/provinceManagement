function send_email_to_expert(){
  $("#expert_email_error_message").empty();
  Dajaxice.adminStaff.ExpertDispatch(ExpertDispatch_callback,{'form':$('#expert_email_send_form').serialize(true)});
}
function ExpertDispatch_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    $.each(data.field,function(i,item){
      object = $('#'+item);
      object.css("background","white");
    });
    //$("#time_settings_form").css("background","white");
    $("#expert_email_error_message").append("<strong>"+data.message+"</strong>");
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

function remove_expert(email){
	var email = email
	Dajaxice.adminStaff.RemoveExpert(remove_expert_callback,{'email':email});
}

function remove_expert_callback(data){
	window.location.reload();
}	
function import_expert(){
  $("#expert_email_error_message").empty();
  Dajaxice.adminStaff.ExpertImport(ExpertImport_callback,{'form':$('#expert_email_send_form').serialize(true)});
}
function ExpertImport_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    $.each(data.field,function(i,item){
      object = $('#'+item);
      object.css("background","white");
    });
    //$("#time_settings_form").css("background","white");
    $("#expert_email_error_message").append("<strong>"+data.message+"</strong>");
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
    // if success all field background turn into white
    $.each(data.field,function(i,item){
      object = $('#'+item);
      object.css("background","white");
    });
    //$("#time_settings_form").css("background","white");
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
