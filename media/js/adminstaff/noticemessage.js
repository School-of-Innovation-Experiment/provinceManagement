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
        if(select.get(0).selectedIndex == 1)
          check.css("display", "none");
        else check.css("display", "");
      }
    }
  );
});

