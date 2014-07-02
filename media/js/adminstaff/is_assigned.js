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
    alert("here");
    Dajaxice.adminStaff.first_round_recommend(first_round_callback, {});
}
function first_round_callback(data){
    
}
