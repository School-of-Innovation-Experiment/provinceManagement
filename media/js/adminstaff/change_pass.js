function change(username)
{
    if(confirm("您确定要重置用户 "+ username+" 的密码？"))
    {
      Dajaxice.adminStaff.change_pass(change_callback,{"username":username});
    }
}

function change_callback(data)
{
  if(data.has_changed)
  {
    alert("重置成功！已重置为： 123456");
  }
  else
  {
    alert("重置失败！");
  }
}
