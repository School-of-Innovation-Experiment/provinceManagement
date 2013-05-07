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
$(function()
  {
    $("#proj_cate_select").change(proj_cate_select_onchange);
  }
 );
