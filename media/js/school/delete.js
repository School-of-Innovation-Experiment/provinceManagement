/* file delete operation*/

$(document).ready(function(){
  $("div#delete-error-panel").hide();
});

$('[rel="file_delete"]').click(function(){
  
  var pid = $(this).attr("pid");
  var fid = $(this).attr("fid");
  Dajaxice.school.FileDeleteConsistence(file_delete_callback,
                                        {'pid':pid, 'fid':fid});
});

function file_delete_callback(data){
  if(data.is_deleted === true){
      var fid = "tr[id=" + data.fid +"]";
      console.log("successs!");
      console.log(data.message);
      console.log(fid);
      $(fid).remove();
    }
  else{
      console.log("Failed!");
      console.log(data.message);
      $("div#delete-error-panel").show();
      $("p#delete-message").text(data.message);

  }
}

$('[rel="student_delete"]').click(function(){
  
  var uid = $(this).attr("uid");
  Dajaxice.school.StudentDeleteConsistence(student_delete_callback,
                                         {'uid':uid});
});

function student_delete_callback(data){
  if(data.is_deleted == true){
      var uid = "tr[id=" + data.uid +"]";
      console.log("successs!");
      console.log(data.message);
      console.log(uid);
      $(uid).remove();
    }
  else{
      console.log("Failed!");
      console.log(data.message);
      $("div#delete-error-panel").show();
      $("p#delete-message").text(data.message);
  }
}
