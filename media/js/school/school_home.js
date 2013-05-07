function financial_cate_select_onchange(select)
{
  Dajaxice.school.FinancialCateChange(financial_cate_change_callback
                                      , {"cate": $("#financial_cate_select").val()});
}
function financial_cate_change_callback(data){
  var error = $("#error_message");
  error.empty();
  error.append(data.message);
  // alert(data.message);
}
$(function()
  {
    $("#financial_cate_select").change(financial_cate_select_onchange);
  }
 );
