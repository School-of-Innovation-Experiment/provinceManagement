function proj_cate_select_onchange(select)
{
  Dajaxice.school.ProjCateChange(proj_cate_change_callback
                                 , {"cate": $("#proj_cate_select").val()});
}

function proj_cate_change_callback(data){
  var error = $("#error_message");
  error.empty();
  error.append(data.message);
  // alert(data.message);
}
function proj_insitute_select_onchange(select)
{
  Dajaxice.school.ProjInsituteChange(proj_insitute_change_callback
                                 , {"cate": $("#proj_insitute_select").val()});
}

function proj_insitute_change_callback(data){
  var error = $("#insitute_error_message");
  error.empty();
  error.append(data.message);

  // alert(data.message);
}
$(function()
  {
    $("#proj_cate_select").change(proj_cate_select_onchange);
    $("#proj_insitute_select").change(proj_insitute_select_onchange);
  }
 );
