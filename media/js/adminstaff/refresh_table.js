function insitute_select_onchange(){
    var select = $("#id_insitute_choice").val();
    Dajaxice.adminStaff.refresh_alloc_table(refresh_alloc_table_callback, {"insitute": select});
}
function refresh_alloc_table_callback(data){
    $("#subjectalloc_table").html(data.table); 
}
$(function(){
    $("#id_insitute_choice").change(insitute_select_onchange);   
});
