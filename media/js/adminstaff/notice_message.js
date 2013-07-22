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
  Dajaxice.adminStaff.TemnoticeChange(add_or_update_notice_callback);
  
}
function add_or_update_notice_callback(data){
  alert("111111");
  change_id="";
  if(data.status == "2") {
  }
  else if(data.status == "0") {
    $("#member_group_table").html(data.table);
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
  change_id    = $(tr_parent).children("td:eq(0)").html();
  $("#template_notice_info_form").find("#title").val(text_title);
  $("#template_notice_info_form").find("#message").val(text_message);

}
function delete_notice_id(noticeId){
  change_id = noticeId;
}
function cancel_change() {
  change_id = "";
}
