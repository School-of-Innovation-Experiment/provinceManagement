function score_submit_check(){
    var flag = false;

	sc_significant = $("#id_score_significant").val();
	if(sc_significant < 0 || sc_significant > 15){
        flag = true;
        $("#id_score_significant").css("background","red");
    }

    sc_value = $("#id_score_value").val();
    if (sc_value < 0 || sc_value> 20){
        flag = true;
        $("#id_score_value").css("background","red");
    }

    sc_innovation = $("#id_score_innovation").val();
    if (sc_innovation < 0 || sc_innovation > 25){
        flag = true;
        $("#id_score_innovation").css("background","red");
    }

    sc_practice = $("#id_score_practice").val();
    if (sc_practice < 0 || sc_practice > 20){
        flag = true;
        $("#id_score_practice").css("background","red");
    }
    sc_achievement = $("#id_score_achievement").val();
    if (sc_achievement < 0 || sc_achievement > 10){
        flag = true;
        $("#id_score_achievement").css("background","red");
    }
    sc_capacity = $("#id_score_capacity").val();
    if (sc_capacity < 0 || sc_capacity > 10){
        flag = true;
        $("#id_score_capacity").css("background","red");
    }
    if (flag){
        $("#id_alert").attr("class", "alert alert-error");
        $("#id_alert").html("<strong>分数输入有误，请阅读“打分须知”后，重新填写</strong>");
    }
    return !flag;
}
