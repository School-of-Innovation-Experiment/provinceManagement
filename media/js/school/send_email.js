function send_email_to_teacher(){
  $("#teacher_email_error_message").empty();
  Dajaxice.school.TeacherDispatch(teacherDispatch_callback,{'form':$('#Teacher_email_send_form').serialize(true)});
}
function teacherDispatch_callback(data){
  if (data.status == "1"){
    // if success all field background turn into white
    $.each(data.field,function(i,item){
      object = $('#'+item);
      object.css("background","white");
    });
    //$("#time_settings_form").css("background","white");
    $("#teacher_email_error_message").append("<strong>"+data.message+"</strong>");
  }
  else
  {
    $.each(data.field,function(i,item){
      object = $('#'+item);
      object.css("background","white");
    });
    //error field background turn into red
    $.each(data.error_id,function(i,item){
      alert(item);
      object = $('#'+item);
      object.css("border-color","red");
    });
    $("#teacher_email_error_message").append("<strong>"+data.message+"</strong>");
  }
}
