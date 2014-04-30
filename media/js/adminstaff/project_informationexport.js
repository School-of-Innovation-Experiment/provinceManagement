function releaseexcel_callback(data){
  location.href = data.path;
  $('#excelprogress').modal('hide');
}

function releaseexcel_expertscore(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Release_Excel(releaseexcel_baseinformation_callback,{'exceltype':2});
}

function releaseexcel_projectsummary(){
  $('#excelprogress').modal('show');
  Dajaxice.adminStaff.Release_Excel(releaseexcel_baseinformation_callback,{'exceltype':3});
}
