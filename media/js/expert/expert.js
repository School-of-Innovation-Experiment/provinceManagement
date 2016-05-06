function submit_score(pid)
{
    var score=$('#score').val();
    var pid=pid;
    Dajaxice.expert.expert_score(score_callback,{'pid':pid,'score':score});
    return false;
}
function score_callback(data)
{
    if(data=="ValueError")
        alert("请检查输入内容！");
    else if(data=="QueryError")
        alert("评分失败，请重新评分！");
    else if(data=="ScoreError")
        alert("请输入有效评分(0-100)！");
    else if(data=="SUCCESS")
    {
        var redirect=confirm("评分成功！点击好返回项目列表，点击取消停留本页面。");
        if(redirect)
        {
            window.location="/expert";
        }
    }
    else
    {
        alert("未知错误，请重新评分！");
    }
}
