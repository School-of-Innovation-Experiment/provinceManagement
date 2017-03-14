var glo_project_id;
function get_subject_id(project_id){
  glo_project_id = project_id;
}
function applicaton_control(){
  Dajaxice.adminStaff.applicaton_control(applicaton_control_callback,{});
}

function applicaton_control_callback(data){
  if (data.flag == 0){
    $('#application_button').attr("class","btn btn-primary");
    $('#application_button').val("打开申请");
    $('#applying-information').text("项目申请开关处于关闭状态,学生不能进行填报");    
  }
  else if(data.flag == 1)
  {
    $('#application_button').attr("class","btn btn-warning");
    $('#application_button').val("关闭申请");
    $('#applying-information').text("项目申请开关处于打开状态,若各学院也为打开状态,则学生可以进行填报");
  }
  else
  {
    alert(data.message);
  }
}

function switch_category()
{
    var rs = $('#switch_result');
    var id = $('#switch_project_id').val();
    var cate = $('#switch_type_name').val();
    Dajaxice.adminStaff.switch_category(switch_category_callback,
                                        {'pid': id, 'cname': cate})
}

function switch_category_callback(data)
{
    var rs = $('#switch_result');
    if(data.status == 0)
    {
        rs.attr("class", "label label-success");
        rs.html("更新成功!");
    }
    else 
    {
        rs.attr("class", "label label-important");
        if(data.status == 1)
            rs.html("更新失败，无该项目!");
        else if(data.status == 2)
            rs.html("更新失败，无此类型！");
        else if(data.status == 3)
            rs.html("更新失败，此项目为创业类项目！");
        else
            rs.html("未知错误!");
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
  Dajaxice.adminStaff.finish_control(finish_control_callback,{"year_list":year_list});
}

function auto_finish(){
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
  Dajaxice.adminStaff.auto_finish(auto_finish_callback,{"year_list":year_list});
}

function auto_finish_callback(data)
{
    var content;
    if(data.flag == 0)
    {
        content = "以下年份自动结题操作成功:\n";
        for (var i = 0; i < data.auto_finished.length - 1; i++) {
            content += data.auto_finished[i] + "\n";
        };
        content += data.auto_finished[data.auto_finished.length - 1];
    }
    else
    {
        content = '自动结题失败,请联系管理员操作';
    }
    alert(content);
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
  Dajaxice.adminStaff.change_project_overstatus(change_overstatus_callback,{'project_id':glo_project_id,"changed_overstatus":overstatus});
}
function change_overstatus_callback(data){
  var target = "#overstatus_" + glo_project_id;
  $(target).html(data.res);
}

$('[rel="isover"]').click(function(){
  var pid = $(this).attr("pid");
  Dajaxice.school.isover_control(isover_control_callback,{"pid":pid});
});

function isover_control_callback(data){
  var pid = data.pid;
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
function project_code_add(){
  var project_unique_code = $('#project_code_add').find('#project_code').val().trim();
  Dajaxice.adminStaff.change_project_unique_code(change_projectuniquecode_callback,{'project_id':glo_project_id,"project_unique_code":project_unique_code});
}
function get_project_unique_code(caller){
  glo_project_id = $(caller).attr('pid');
  var project_unique_code = $(caller).parent().text().trim();
  $('#project_code_add').find('#project_code').val(project_unique_code);
}

function set_recommend_rate(){
    set_val = $("#id_rec_setting").val()
    $("#warning_bar").hide();
    $("#success_bar").hide();
    Dajaxice.adminStaff.set_recommend_rate(set_recommend_rate_callback, {'set_val': set_val})
}
function set_recommend_rate_callback(data){
    if(data.message == "wrong input"){
        $("#warning_bar").show();
    }
    else{
        $("#current_rate").html("项目推荐比例管理（当前比例:" + data.set_val + "%）");
        $("#success_bar").show();
    }
}
function change_projectuniquecode_callback(data){
    if(data.res == "error"){
        alert("格式不合法或相同编号已存在");
    }
    else{
        var target = "#ProjectUniqueCode_" + glo_project_id;
        $(target).html(data.res);
    }
}
function auto_ranking(){
    $("#success_bar_2").hide();
    if(confirm("将对当届所有项目编号，若存在项目原有编号，本次操作后将覆盖，是否继续？"))
        Dajaxice.adminStaff.auto_ranking(auto_ranking_callback, {});
}
function auto_ranking_callback(data){
    $("#success_bar_2").show();
}

function download(filetype){
    Dajaxice.adminStaff.download_zipfiles(download_callback,{"filetype":filetype,'project_manage_form':$('#project_manage_form').serialize(true)})
}

function download_callback(data){
   location.href = data.path; 
}
