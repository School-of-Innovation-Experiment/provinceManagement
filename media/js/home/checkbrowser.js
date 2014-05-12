function getOs()
{
  var checkerror=false;
  var u_agent = navigator.userAgent;
  if(u_agent.indexOf("Safari")>-1 || u_agent.indexOf("Firefox")>-1 || window.opera){
  }else if(u_agent.indexOf("MSIE 6.0")>-1 ||u_agent.indexOf("MSIE 7.0")>-1 ){
    alert("为了达到最佳浏览效果，我们推荐您使用以下浏览器 请使用'谷歌浏览器'或'火狐浏览器'");
  }else{
    $('#myModal').modal('show');
  }
}
window.onload = getOs;
