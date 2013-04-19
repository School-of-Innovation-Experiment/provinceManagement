function send_email_to_student(){
    $("#student_email_error_message").empty();
    Dajaxice.teacher.StudentDispatch(studentDispatch_callback,{'form':$('#student_email_send_form').serialize(true)});
    }
function studentDispatch_callback(data){
    if (data.status == "1"){
        // if success all field background turn into white
        $.each(data.field,function(i,item){
                object = $('#'+item);
                object.css("background","white");
                });
        //$("#time_settings_form").css("background","white");
        $("#student_email_error_message").append("<strong>"+data.message+"</strong>")
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
            $("#student_email_error_message").append("<strong>"+data.message+"</strong>")
        }
    }
