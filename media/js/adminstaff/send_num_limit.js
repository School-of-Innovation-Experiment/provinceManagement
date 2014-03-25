function send_num_limit(){
  $("#num_limit_error_message").empty();
  Dajaxice.adminStaff.NumLimit(limitednum_callback,{'form':$('#num_limit_form').serialize(true)});
};
$('[rel="project_limit_num_reset"]').click(function() {
  var bln = window.confirm("是否确认重置所有项目数量限制？（此操作不可撤销）");
  if(bln) {
    location.href = "ProjectLimitNumReset";
  }
});
function limitednum_callback(data){
  if (data.status == "1"){
    $("#limited_num").css("background","white");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
  }
  else
  {
    id = data.id;
    object = $('#'+id);
    object.css("background","red");
    $("#num_limit_error_message").append("<strong>"+data.message+"</strong>");
  }
};
