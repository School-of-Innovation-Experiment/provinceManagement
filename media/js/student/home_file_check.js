function empty_file_set_check(){
   Dajaxice.student.empty_file_set_check(check_call_back, {});
}
function check_call_back(data){
    if(data.status == "empty"){
        $("#warning_modal").modal();
    }
}
