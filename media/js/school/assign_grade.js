var success_msg = '<span class="label label-success">设置成功</span>';
$(function(){
    $('.assign_grade').change(function(){
        var grade = $(this).val();
        var pid = $(this).attr('pid');
        Dajaxice.school.update_project_grade(update_project_grade_callback,
            {
                'grade_num': grade,
                'project_id': pid,
            });
    });
    function update_project_grade_callback(data)
    {
        if(data.status == 0)
            window.location.reload();
        else
        {
            if(data.status == 1)
                alert('未知错误');
            else if(data.status == 2)
                alert('非法类别');
            else if(data.status == 3)
                alert('无权限修改');
            else if(data.status == 4)
                alert('达到该类申报最大数量');
            else if(data.status == 5)
                alert('不在申报时间内，禁止使用该功能!');
            window.location.reload();
        }
    }
});
