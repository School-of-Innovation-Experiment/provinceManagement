function student_code_project_query(){
    var student_code = $("#student_code_input").val();
    Dajaxice.adminStaff.student_code_project_query(query_callback, {"student_code": student_code});
}
function query_callback(data){
    if(data.message == "ok"){
        $("#result_table").html(data.table);
    }
    else{
        $("#result_table").html('<br \><div class="alert alert-warning">正在进行中的项目没有与该学号关联的对象存在</div>');
    }
}
