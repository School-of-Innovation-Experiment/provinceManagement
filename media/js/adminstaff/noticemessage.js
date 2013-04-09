$("#noticemessage_form").onsubmit = function (){
  if($("#select_role").get(0).selectedIndex == 0)
  {
    $("#noticemessage_warning");
    return false;
  }
}
