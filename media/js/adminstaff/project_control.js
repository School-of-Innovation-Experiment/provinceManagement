function finish_control(){
  var year_list=new Array();
  var j=0;
  var checkBoxs = document.getElementsByTagName("input");//取得input标签的对象
  for(var i=0; i<checkBoxs.length; i++)
  {
    if(checkBoxs[i].type=="checkbox" && checkBoxs[i].checked)
    {
      year_list[j]=checkBoxs[i].value;
      j++;   
    }
  }
  Dajaxice.adminStaff.finish_control(finish_control_callback,{"year_list":year_list});
}

function finish_control_callback(data){
  if (data.flag == 0){
    $('#finish_button').attr("class","btn btn-primary");
    $('#finish_button').val("打开结题");
    alert("已经关闭结题，学生现在不能填报结题报告");
  }
  else if(data.flag == 1)
  {
    //警告样式，只可筛选
    $('#finish_button').attr("class","btn btn-warning");
    $('#finish_button').val("关闭结题");
    alert("已经打开结题，学生现在能填报结题报告");
  }
  else
  {
    alert(data.message);
  }
}