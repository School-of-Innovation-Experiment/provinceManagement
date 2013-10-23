var glob_email;

function get_email(email){
    glob_email = email;
}
function brute_delete(){
    Dajaxice.teacher.brute_delete(brute_delete_callback,{'email': glob_email});
}
function brute_delete_callback(data){
    var target_tr = "[name='" + "tr_" + glob_email + "']";
    $(target_tr).remove();
}
function simple_delete(email){
    glob_email = email;
    Dajaxice.teacher.simple_delete(simple_delete_callback,{'email': email});
}
function simple_delete_callback(data){
    var target_tr = "[name='" + "tr_" + glob_email + "']";
    $(target_tr).remove();
}
