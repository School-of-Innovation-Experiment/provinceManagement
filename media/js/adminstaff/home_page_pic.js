$(document).ready(function(){
  $("div#delete-error-panel").hide();
});

$('[rel="file_delete"]').click(function(){
  var fid = $(this).attr("fid");
  Dajaxice.adminStaff.FileDeleteConsistence(file_delete_callback,
                                        {'fid':fid});
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
