function send_email_to_student(){
    $("#student_email_error_message").empty();
    Dajaxice.school.StudentDispatch(StudentDispatch_callback,{'form':$('#student_email_send_form').serialize(true)});
    }
function StudentDispatch_callback(data){
    if (data.status == "1"){
        // if success all field background turn into white
        $.each(data.field,function(i,item){
                object = $('#'+item);
                object.css("background","white");
                });
        $("#student_email_error_message").append("<strong>"+data.message+"</strong>")
         
        //$("#remaining_activation_times").empty();
        //$("#remaining_activation_times").append("<strong>"+''+data.remaining_activation_times+''+"</strong>")
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

function send_email_to_students()
{
    var emails = $('#multi_emails').val();
    var students_array = emails.split('\n');
    var pattern =  /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
    var email_name = new Array();
    for(var i = 0; i < students_array.length; i++)
    {
        var item = students_array[i].split(' ');
        var email = item[0];
        if(item.length != 2)
        {
            alert('填写格式错误:' + students_array[i]);
            return;
        }
        else if(!pattern.test(email))
        {
            alert('邮箱格式错误:' + email);
            return;
        }
        email_name.push(item);
    }
    Dajaxice.school.StudentsDispatch(students_dispatch_callback, {'emails': email_name});
}

function students_dispatch_callback(data)
{
    if(data.status == 0)
        alert('发送成功!');
    else if(data.status == 1)
    {
        var msg = '发送中途失败!原因:\n' + data.reason;
        msg += '\n相关信息:\n邮箱:'+data.context.email+'\n负责人:'+data.context.name;
        alert(msg);
    }
    else if(data.status == 2)
    {
        var msg = '发送中途出现错误!原因可能是该邮箱已被使用或激活邮件服务器出现问题,';
        msg += '若您确认邮箱无误且频繁得到该类错误，请联系系统管理员。';
        msg += '\n相关邮箱:\n';
        for(var i = 0; i < data.emails.length; i++)
            msg += data.emails[i] + '\n';
        alert(msg);
    }
}
