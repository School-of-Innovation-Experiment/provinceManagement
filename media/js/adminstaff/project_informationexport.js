function releaseexcel_callback(data){
  location.href = data.path;
  $('#excelprogress').modal('hide');
}
function export_excel(exceltype) {
    $('#excelprogress').modal('show');
    Dajaxice.adminStaff.Release_Excel(releaseexcel_callback,{'exceltype':exceltype,'project_manage_form':$('#project_manage_form').serialize(true)});

}

