var change_id = "";
$(function(){
  var form = $("#noticemessage_form");
  var select = $("#select_role");
  var error = $("#noticemessage_warning");
  var check = $("#message_check");
  form.submit(
    function (){
      if(select.get(0).selectedIndex == 0)
      {
        error.css("display","");
        select.css("border-color", "#b94a48");
        return false;
      }
      return true;
    });
  select.change(
    function (){
      if(select.get(0).selectedIndex == 0)
      {
        select.css("border-color", "#b94a48");
        check.css("display", "none");
      }
      else
      {
        select.css("border-color", "#cccccc");
        if(select.get(0).selectedIndex == 1 || select.get(0).selectedIndex == 3)
          check.css("display", "none");
        else check.css("display", "");
      }
    }
  );
});

function add_or_update_notice(){

  $("#template_notice_error_message").empty();


  Dajaxice.adminStaff.TemNoticeChange(add_or_update_temnotice_callback,
                                      {'form': $('#template_notice_info_form').serialize(true),
                                       'origin': change_id});
  
}
function add_or_update_temnotice_callback(data){
  change_id="";
  if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  else if(data.status == "0") {
    $("#temlate_notice_table").html(data.table);
  }
  $("#template_notice_error_message").append("<strong>"+data.message+"</strong>");

}
function select_template_notice(caller){
  text_message=$(caller).parent().parent().parent().children("td:eq(2)").html();
  $("#textarea").val(text_message);
}
function get_template_notice(caller){
  tr_parent = $(caller).parent().parent().parent();
  text_title   = $(tr_parent).children("td:eq(1)").html();
  text_message = $(tr_parent).children("td:eq(2)").html();
  change_id    = $(tr_parent).children("td:eq(0)").attr('id');
  $("#template_notice_info_form").find("#title").val(text_title);
  $("#template_notice_info_form").find("#message").val(text_message);
}
function get_template_notice_id(noticeId){
  change_id = noticeId;
}
function delete_template_notice()
{
  $("#template_notice_error_message").empty();
  Dajaxice.adminStaff.TemNoticeDelete(add_or_update_temnotice_callback,
                                {'deleteId': change_id});
}


function cancel_change() {
  change_id = "";
}
function empty_notice_profile_info(){
  $("#template_notice_info_form").find("#title").val("");
  $("#template_notice_info_form").find("#message").val("");
}

