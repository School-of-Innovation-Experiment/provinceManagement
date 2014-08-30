function student_code_project_query(){
    var student_code = $("#student_code_input").val();
    alert(student_code);
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

function delete_project_query(){
    var delete_info = $("#delete_info_input").val();
    Dajaxice.adminStaff.delete_project_query(delete_query_callback, {"delete_info": delete_info});
}
function delete_query_callback(data){
    if(data.message == "ok"){
        $("#delete_result_table").html(data.table);
    }
    else{
        $("#delete_result_table").html('<br \><div class="alert alert-warning">正在进行中的项目没有与该学号关联的对象存在</div>');
    }
}

function delete_project_id(pid){
    Dajaxice.adminStaff.delete_project_id(delete_project_id_callback,{"pid":pid});
}

function delete_project_id_callback(data){
    if(data.message == "ok"){
        var fid = "tr[id=" + data.pid +"]";
        $(fid).remove();
    }
}
