$(function(){
  var form = $("#noticemessage_form");
  var select = $("#select_role");
  var error = $("#noticemessage_warning");
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
        }
      else
      {
        select.css("border-color", "#cccccc");
      }
    }
  );
});

