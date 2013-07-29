function applicaton_control(){
	Dajaxice.school.applicaton_control(applicaton_control_callback,{});
}

function applicaton_control_callback(data){
  if (data.flag == 0){
    $('#application_button').attr("class","btn btn-primary");
    $('#application_button').val("打开申请");
    alert("已经关闭申请，学生现在不能填报申请书");
  }
  else if(data.flag == 1)
  {
    //警告样式，只可筛选
    $('#application_button').attr("class","btn btn-warning");
    $('#application_button').val("关闭申请");
    alert("已经打开申请，学生现在能填报申请书");
  }
  else
  {
    alert(data.message);
  }
}