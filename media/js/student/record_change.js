
function add_or_update_record() {
  
  $("#record_error_message").empty();
  Dajaxice.student.recordChange(add_or_update_record_callback,
                                {'form':$('#process_record_info_form').serialize(true)
                                });
};

function add_or_update_record_callback(data) {
    if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  else if(data.status == "0") {
    $("#record_group_table").html(data.table);
  }
  $("#record_error_message").append("<strong>"+data.message+"</strong>");
};