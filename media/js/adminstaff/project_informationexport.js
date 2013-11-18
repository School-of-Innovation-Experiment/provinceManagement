function releaseexcel_baseinformation(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Release_Excel(releaseexcel_baseinformation_callback,{'exceltype':1});
}
function releaseexcel_baseinformation_callback(data){
	location.href = data.path
	$('#excelprogress').modal('hide');
}

function releaseexcel_expertscore(){
  $('#excelprogress').modal('show');
  alert("haha");
  Dajaxice.adminStaff.Release_Excel(releaseexcel_baseinformation_callback,{'exceltype':2});
}