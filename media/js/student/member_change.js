var change_id = "";
function add_or_update_member() {
  $("#teacher_email_error_message").empty();
  Dajaxice.student.MemberChange(add_or_update_member_callback,
                                {'form': $('#member_change_form').serialize(true),
                                 'origin': change_id});
};

function add_or_update_member_callback(data) {
  change_id = "";
  if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  else if(data.status == "0") {
    $("#member_group_table").html(data.table);
  }
  $("#teacher_email_error_message").append("<strong>"+data.message+"</strong>");
};

function change_member(caller)
{
  $("#teacher_email_error_message").empty();
  change_id = $(caller).parent().parent().children("td").first("td").html();
  $("#teacher_email_error_message").append("<strong>"+"更换队员：" +change_id+"</strong>");
};

function delete_member(caller)
{
  $("#teacher_email_error_message").empty();
  delete_id = $(caller).parent().parent().children("td").first("td").html();
  Dajaxice.student.MemberDelete(add_or_update_member_callback,
                                {'deleteId': delete_id});
}

function get_student_info(studentId)
{
  $("#change_info_student_id").html(studentId);
  change_id = studentId;
}

function cancel_change() {
  change_id = "";
}

function change_member_info()
{
  $("#teacher_email_error_message").empty();
  Dajaxice.student.MemberChangeInfo(add_or_update_member_callback,
                                {'form': $('#member_change_info_form').serialize(true),
                                 'origin': change_id});
}
