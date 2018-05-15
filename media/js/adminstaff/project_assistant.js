var glo_project_id;
function get_subject_id(project_id){
    glo_project_id = project_id;
}

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

function changeyear_project_query(){
    var changeyear_info = $("#changeyear_info_input").val();
    Dajaxice.adminStaff.changeyear_project_query(changeyear_query_callback, {"changeyear_info": changeyear_info});
}
function changeyear_query_callback(data){
    if(data.message == "ok"){
        $("#changeyear_result_table").html(data.table);
    }
    else{
        $("#changeyear_result_table").html('<br \><div class="alert alert-warning">正在进行中的项目没有与该教师关联的对象存在</div>');
    }
}

function subject_grade(){
    var changed_grade = $('#id_subject_grade').find("option:selected").val();
    Dajaxice.adminStaff.change_subject_grade(change_grade_callback,{'project_id':glo_project_id,"changed_grade":changed_grade});
}
function change_grade_callback(data){
    var target = "#gradeid_" + glo_project_id;
    $(target).html(data.res);
}

function changeyear_project_id(pid){
    var value = $('#year_select_'+ pid +'  option:selected').val();
    Dajaxice.adminStaff.changeyear_project_id(changeyear_project_id_callback,{"pid":pid, "year":value});
}

function changeyear_project_id_callback(data){
    if(data.message == "ok"){
        var fid = "td[id=" + data.pid +"]";
        $(fid)[0].innerHTML = data.year;
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

var tmp = "";
function get_current_year(pid){
  if(tmp != pid){
      var myDate = new Date();
      var year = myDate.getFullYear();
      var select_id = "year_select_" + pid;
      $("select[id=" + select_id + "]").empty();
      $("select[id=" + select_id + "]").append("<option value='年份' selected>年份</option>");
      $("select[id=" + select_id + "]").append("<option value='"+(year+1)+"'>"+(year+1)+"</option>");
      $("select[id=" + select_id + "]").append("<option value='"+year+"'>"+year+"</option>");
      $("select[id=" + select_id + "]").append("<option value='"+(year-1)+"'>"+(year-1)+"</option>");
      $("select[id=" + select_id + "]").append("<option value='"+(year-2)+"'>"+(year-2)+"</option>");
      $("select[id=" + select_id + "]").append("<option value='"+(year-3)+"'>"+(year-3)+"</option>");
      $("select[id=" + select_id + "]").append("<option value='"+(year-4)+"'>"+(year-4)+"</option>");
      tmp = pid;
  }

}
