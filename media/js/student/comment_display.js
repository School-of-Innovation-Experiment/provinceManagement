function comment_show_checker(is_show){
    if(is_show == "True"){
        if($("#id_inspector_comments").val().length == 0){
            $("#id_inspector_comments").hide();
            $("#id_comment_warning").show();
        }
        else{
            $("#id_inspector_comments").attr("readonly", true);
        }
    }
}
