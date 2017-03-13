var glo_project_id;
function get_subject_id(project_id){
  glo_project_id = project_id;
}
function applicaton_control(){
  Dajaxice.school.applicaton_control(applicaton_control_callback,{});
}

function applicaton_control_callback(data){
  if (data.flag == 0){
    $('#application_button').attr("class","btn btn-primary");
    $('#application_button').val("打开申请");
    //alert("已经关闭申请，学生现在不能填报申报书");
    $('#applying-information').text("项目申请开关处于关闭状态,学生不能进行填报");    
  }
  else if(data.flag == 1)
  {
    //警告样式，只可筛选
    $('#application_button').attr("class","btn btn-warning");
    $('#application_button').val("关闭申请");
    //alert("已经打开申请，学生现在能填报申报书");
    $('#applying-information').text("项目申请开关处于打开状态,若学校也为打开状态,则学生可以进行填报");
  }
  else
  {
    alert(data.message);
  }
}

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
  Dajaxice.school.finish_control(finish_control_callback,{"year_list":year_list});
}

function finish_control_callback(data){
  if (data.flag == 0){
    $('#finish_button').attr("class","btn btn-primary");
    $('#finish_button').val("打开结题");
    $("input[name='check_box_list']").each(function(){
       $(this).prop("checked",false);
    });
	$('#year_finishing_span').text("目前没有打开结题开关");
    //alert("已经关闭结题，学生现在不能填报结题报告");
    $('#finishing-information').hide();
  }
  else if(data.flag == 1)
  {
    //警告样式，只可筛选
    $('#finish_button').attr("class","btn btn-warning");
    $('#finish_button').val("关闭结题");
    var content = "结题开关已开启，目前处于结题状态的项目年份是：";
    for (var i = 0; i < data.year_finishing_list.length; i++) {
      content += ("( "+ data.year_finishing_list[i] + " )");
    };
    $('#year_finishing_span').text(content);
    //alert("已经打开结题，学生现在能填报结题报告");
    $('#finishing-information').show();
    $('#finishing-information').text("点击“关闭结题按钮”会取消所有结题年份");
  }
  else
  {
    alert(data.message);
  }
}

function project_overstatus(){
  var overstatus = $('#overstatus_choice').find("option:selected").val();
  Dajaxice.school.change_project_overstatus(change_overstatus_callback,{'project_id':glo_project_id,"changed_overstatus":overstatus});
}
function change_overstatus_callback(data){
  var target = "#overstatus_" + glo_project_id;
  $(target).html(data.res);
}
$('[rel="isover"]').click(function(){
  var pid = $(this).attr("pid");
  Dajaxice.school.isover_control(isover_control_callback,{"pid":pid});
})

function isover_control_callback(data){
  pid = data.pid;
  if (data.flag == 1){
    $('#'+pid).attr("class","btn btn-primary");
    $('#'+pid).val("打开结题");
    alert("已经关闭项目");
  }
  else if(data.flag == 0)
  {
    //警告样式，只可筛选
    $('#'+pid).attr("class","btn btn-warning");
    $('#'+pid).val("关闭结题");
    alert("已经打开项目");
  }
  else
  {
    alert(data.message);
  }
}
