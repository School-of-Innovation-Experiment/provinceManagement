function send_num_limit(){
  $("#num_limit_error_message").empty();
  Dajaxice.adminStaff.NumLimit(limitednum_callback,{'form':$('#num_limit_form').serialize(true)});
}
function limitednum_callback(data){
  if (data.status == "1"){
    $("#limited_num").css("background","white");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
    $("#numlimit_table").html(data.table);
  }
  else
  {
    id = data.id;
    object = $('#'+id);
    object.css("border-color","red");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
  }
}
