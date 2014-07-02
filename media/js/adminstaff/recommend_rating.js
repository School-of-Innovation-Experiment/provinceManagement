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
