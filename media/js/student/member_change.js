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

function delete_member()
{
  $("#teacher_email_error_message").empty();
  // delete_id = $(caller).parent().parent().children("td").first("td").html();
  Dajaxice.student.MemberDelete(add_or_update_member_callback,
                                {'deleteId': change_id});
}

function get_student_info(caller)
{
  var  tr_parent= $(caller).parent().parent();
  change_id   =  $(tr_parent).children("td").first("td").html();
  $("#change_info_student_id").html(change_id);
  $("select[name='sex']").val($(tr_parent).children("td:eq(2)").attr('val'));
  $("input[name='nation']").val($(tr_parent).children("td:eq(3)").html());
  $("input[name='email']").val($(tr_parent).children("td:eq(4)").html());
  $("input[name='telephone']").val($(tr_parent).children("td:eq(5)").html());
  $("input[name='classInfo']").val($(tr_parent).children("td:eq(9)").html());
  $("select[name='school']").val($(tr_parent).children("td:eq(6)").attr('val'));
  $("select[name='major']").val($(tr_parent).children("td:eq(7)").attr('val'));
  // $("input[name='major']").val($(tr_parent).children("td:eq(7)").html());
  $("input[name='grade']").val($(tr_parent).children("td:eq(8)").html());
}
function get_student_deleteid(caller)
{
  var  tr_parent= $(caller).parent().parent();
  change_id   =  $(tr_parent).children("td").first("td").html();
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
