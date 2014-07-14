function release_excel(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Release_Excel(release_excel_callback);
}
function release_excel_callback(data){
	location.href = data.path
	$('#excelprogress').modal('hide');
}
