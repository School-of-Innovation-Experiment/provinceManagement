function release_excel(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Release_Excel(release_excel_callback);
}
function release_excel_callback(data){
	location.href = data.path
	$('#excelprogress').modal('hide');
}

function expert_project_assign(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Expert_Project_Assign(assign_callback);
}

function assign_callback(data){
	$('#excelprogress').modal('hide');
    alert(data);
}
