function project_sync(){
  var project_sync_list=new Array();
  var j=0;
  var sync_username = $("#Sync_username").val();
  var sync_password = $("#Sync_password").val();
  if (sync_password==""||sync_username=="")
  {
    alert("用户名或密码不能为空");
  }
  var checkBoxs = $("input[name='check_box']:checked");//取得input标签的对象
  for(var i=0; i<checkBoxs.length&&checkBoxs.length>0; i++)
  {
      project_sync_list[j]=checkBoxs[i].value;
      j++;
  }
  Dajaxice.adminStaff.project_sync(project_sync_callback,{"project_sync_list":project_sync_list,'username':sync_username,'password':sync_password});
}

function project_sync_callback(data){
  if(data.status=="0")
  {
    alert(data.result);
    // $("#myModal").modal('hide');
    // $("#sync_success_modal").modal('show');
  }
  else if(data.status=="1")
  {
    alert(data.result);
    // $("#myModal").modal('hide');
    // $("#sync_fail_modal").modal('show');
  }
}
