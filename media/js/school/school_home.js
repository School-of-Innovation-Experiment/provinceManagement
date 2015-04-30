var glo_pid
function financial_cate_select_onchange(pid)
{
  glo_pid = pid
  target = "#financial_cate_select" + glo_pid
  Dajaxice.school.FinancialCateChange(financial_cate_change_callback
                                      , {"cate": $(target).val(), "pid": pid});
}
function financial_cate_change_callback(data){
  //var error = $("#error_message" + glo_pid);
  var error = $("#error_message");
  error.show();
  error.empty();
  error.append(data.message);
}

function get_element(caller){
    glo_pid = $(caller).attr('pid');
    project_code = $(caller).parent().text().trim();
    $("#project_code_add").find("#project_code").val(project_code);
}

function project_code_add(){
    project_code = $('#project_code_add').find("#project_code").val().trim();
    Dajaxice.school.change_project_code(change_project_code_callback, {'pid': glo_pid, "project_code": project_code});
}
function change_project_code_callback(data){
    if(data.message == 'error'){
        alert("格式不正确或与已有编号重复...");
    }
    else{
        target = "#ProjectUniqueCode_" + glo_pid;
        $(target).html(data.res);
    }
}

function getPagination(page){
    Dajaxice.school.getPagination(getPaginationCallBack,{
        "page":page,
        "form":$("#schedule_form").serialize(true)
    });
}
function getPaginationCallBack(data){
    $("#project_page").html(data.table);
}
$("#filter_button").click(function(){
    getPagination(1);
});
