function releaseexcel_callback(data){
  location.href = data.path;
  $('#excelprogress').modal('hide');
}

