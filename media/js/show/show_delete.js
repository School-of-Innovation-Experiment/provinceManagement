$("[rel=show_delete]").click(function(){
    Dajaxice.adminStaff.ShowDelete(deleteCallBack, {"uid": $(this).attr("uid"), })
});
function deleteCallBack(data){
    location.reload();
}
