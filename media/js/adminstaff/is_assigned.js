function is_assigned(){
  Dajaxice.adminStaff.judge_is_assigned(is_assigned_callback,{'school':$('#id_school_choice').find("option:selected").val()});
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
    $('#filter_button').val("已经指派专家,只可进行筛选");
  }
  else
  {
    alert(data.message);
  }
}

$(function () {
  $('#id_school_choice').change(is_assigned);
})
