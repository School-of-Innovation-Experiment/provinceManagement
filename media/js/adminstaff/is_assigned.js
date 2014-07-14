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
        alert("初审分级成功");
    }
    else
        alert("分级失败，请联系后台管理员");
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
        alert("初审分级成功");
    }
    else
        alert("分级失败，请联系后台管理员");

}
