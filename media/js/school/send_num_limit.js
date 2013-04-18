function send_num_limit(){
  $("#num_limit_error_message").empty();
  Dajaxice.school.NumLimit(limitednum_callback,{'form':$('#num_limit_form').serialize(true)});
}
function limitednum_callback(data){
  if (data.status == "1"){
    $("#limited_num").css("background","white");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
  }
  else
  {
    id = data.id;
    object = $('#'+id);
    object.css("background","red");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
  }
}
