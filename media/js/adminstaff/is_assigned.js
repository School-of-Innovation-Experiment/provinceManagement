function is_assigned(){
  Dajaxice.adminStaff.judge_is_assigned(is_assigned_callback,{'insitute':$('#id_insitute_choice').find("option:selected").val()});
}

function is_assigned_callback(data){
  if (data.flag == 0){
    $('#filter_button').attr("class","btn btn-primary");
    $('#filter_button').val("没有指定专家，进行指派专家");
  }
  else if(data.flag == 1)
  {
    //警告样式，只可筛选
    $('#filter_button').attr("class","btn btn-warning");
    $('#filter_button').val("已经指派专家,对新添加项目追加分配");
  }
  else
  {
    alert(data.message);
  }
}

function first_round_recommend(){
    if(confirm("请再次确定是否开始本届第一轮推荐分级？（请确认项目是否全部申报完成，专家帐号是否全部导入成功）")){
        $("#excelprogress").modal();
        Dajaxice.adminStaff.first_round_recommend(first_round_callback, {});
    }
}
function first_round_callback(data){
    $("#excelprogress").modal("hide");
    if(data.message = "ok"){
        $("#id_first_round_finish").attr({"class": "btn btn-warning", "onclick": ""})
        $("#id_first_round_finish").html("第一轮推荐分级已结束")
        alert("第一轮分级成功");
    }
    else
        alert("操作失败，请联系后台管理员");
}

function second_round_start(data){
    if(confirm("请再次确定是否开始本届第二轮分配？（请确认第一轮推荐分级是否结束，第二轮专家帐号是否全部导入成功）")){
        $("#excelprogress").modal();
        Dajaxice.adminStaff.second_round_start(second_round_start_callback, {});
    }
}
function second_round_start_callback(data){
    $("#excelprogress").modal("hide");
    if(data.message = "ok"){
        $("#id_second_round_start").attr({"class": "btn btn-warning", "onclick": ""})
        $("#id_second_round_start").html("第二轮分配已结束")
        alert("第二轮分配成功");
    }
    else
        alert("操作失败，请联系后台管理员");
}

function second_round_recommend(){
    if(confirm("请再次确定是否开始本届第二轮推荐分级？（请确认第二轮分配与评审工作是否全部结束）")){
        $("#excelprogress").modal();
        Dajaxice.adminStaff.second_round_recommend(second_round_callback, {});
    }
}
function second_round_callback(data){
    $("#excelprogress").modal("hide");
    if(data.message = "ok"){
        $("#id_second_round_finish").attr({"class": "btn btn-warning", "onclick": ""})
        $("#id_second_round_finish").html("第二轮推荐分级已结束")
        alert("第二轮分级成功");
    }
    else
        alert("操作失败，请联系后台管理员");
}

function show_result(){
    if(confirm("请再次确定是否导出评审结果？（请确认第二轮评审工作全部结束）")){
        $("#excelprogress").modal();
        Dajaxice.adminStaff.show_result(show_result_callback, {});
    }
}
function show_result_callback(data){
    $("#excelprogress").modal("hide");
    if(data.message = "ok"){
        location.href = data.path
        alert("导出成功");
    }
    else
        alert("操作失败，请联系后台管理员");

}

function get_scored_result(forced)
{
    $("#excelprogress").modal("show");
    Dajaxice.adminStaff.scored_result(get_scored_result_callback,{'forced':forced});
}

function get_scored_result_callback(data)
{
    $("#excelprogress").modal("hide");
    setTimeout(function(){scored_result_handler(data)},600);
}
function scored_result_handler(data)
{
    if(data.status == "SUCCESS")
    {
        location.href = data.path;
        alert("导出成功");
    }
    else
    {
        var forced=confirm("操作失败，请再次尝试，错误信息:\n"+data.message+"\n是否确定继续导出？");
        if(forced==true)
            get_scored_result(forced);
    }

}
