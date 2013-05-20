/* file delete operation*/

$('[rel="file_delete"]').click(function(){
  
  var pid = $(this).attr("pid");
  var fid = $(this).attr("fid");
  Dajaxice.school.FileDeleteConsistence(file_delete_callback,
                                        {'pid':pid, 'fid':fid});
});

function file_delete_callback(data){
  if(data.is_deleted === true){
      console.log("successs!");
      console.log(data.message);
    }
  else{
      console.log("Failed!");
      console.log(data.message);
  }
}
