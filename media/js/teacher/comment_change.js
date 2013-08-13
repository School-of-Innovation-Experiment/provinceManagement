var pid;
$(document).ready(function(){
  var strUrl  = location.href.split("/");
  pid     = strUrl[strUrl.length-1];
  
})
function add_or_update_comment() {
  $("#comment_error_message").empty();
  Dajaxice.teacher.commentChange(add_or_update_comment_callback,
                                {'form':$('#process_record_info_form').serialize(true),
                                  'pid':pid
                                });
};

function add_or_update_comment_callback(data) {
  if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  else if(data.status == "0") {
    $("#teacherComment").html(data.table);
  }
  $("#comment_error_message").append("<strong>"+data.message+"</strong>");
};