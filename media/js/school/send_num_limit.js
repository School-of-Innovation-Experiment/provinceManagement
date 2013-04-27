function send_num_limit(){
  $("#num_limit_error_message").empty();
  Dajaxice.school.teacherProjNumLimit(limitednum_callback,
                                      {'form':$('#num_limit_form').serialize(true)});
}
function limitednum_callback(data){
  if (data.status == "1"){    // sucess
    $("#limited_num").css("background","white");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
    $("#projects_remaining").text('剩余数量:'+data["projects_remaining"]);
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
