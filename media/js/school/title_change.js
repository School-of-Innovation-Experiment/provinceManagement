var glo_user_email;
function get_email(email){
  glo_user_email = email;
}
function change_titles(){
  var new_title=document.getElementById("new_title").value;
  Dajaxice.school.title_change(change_titles_callback,{'email':glo_user_email, 'new_title':new_title});
}
function change_titles_callback(data){
  if(data.has_finish == 1)alert("修改成功！");
  else if(data.has_finish == -1)alert("修改失败！此用户邮箱包含多个账户");
  else alert("修改失败！不存在这个邮箱对应的账户！");
  location.reload(true);
}
