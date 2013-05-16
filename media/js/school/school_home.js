var glo_pid
function financial_cate_select_onchange(pid)
{
  glo_pid = pid
  target = "#financial_cate_select" + glo_pid
  Dajaxice.school.FinancialCateChange(financial_cate_change_callback
                                      , {"cate": $(target).val(), "pid": pid});
}
function financial_cate_change_callback(data){
  var error = $("#error_message" + glo_pid);
  error.empty();
  error.append(data.message);
}
