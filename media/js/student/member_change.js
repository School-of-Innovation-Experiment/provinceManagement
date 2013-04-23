function member_change() {
  $("#teacher_meail_error_message").empty();
  Dajaxice.student.MemberChange(memberChange_callback,
                                {'form': $('#member_change_form').serialize(true),
                                 'form2': ''});
};

function memberChange_callback(data) {
  if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  $("#teacher_email_error_message").append("<strong>"+data.message+"</strong>");
};
