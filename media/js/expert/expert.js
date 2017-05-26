function submit_score(pid)
{
    var pass_status=$('#pass_status').prop('checked');
    var pid=pid;
    Dajaxice.expert.expert_score(review_callback,{'pid':pid,'is_pass':pass_status});
    return false;
}
function review_callback(data)
{
    if(data=="Error")
        alert("审核失败,请刷新页面尝试重新提交！");
    else if(data=="SUCCESS")
    {
        var redirect=confirm("审核成功！点击好返回项目列表，点击取消停留本页面。");
        if(redirect)
        {
            window.location="/expert";
        }
    }
    else
    {
        alert("未知错误，请重试！");
    }
}
