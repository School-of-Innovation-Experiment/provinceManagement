$().ready(function(){
  $('#record_table').on("click","div",function(){
    $('#process_record_info_form').find("input[name=weekId]").val($(this).children("h4").attr("val"));
    $('#process_record_info_form').find("input[name=recorder]").val($(this).children("p:eq(0)").attr("val"));
    $('#process_record_info_form').find("textarea[name=recordtext]").val($(this).children("#record_summary").text());
  })
})
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
      $('#process_record_info_form').find("input[name=weekId]").val("");
      $('#process_record_info_form').find("input[name=recorder]").val("");
      $('#process_record_info_form').find("textarea[name=recordtext]").val("");
    }
    $("#record_error_message").append("<strong>"+data.message+"</strong>");
  };
  function delete_record(caller){
    $("#record_error_message").empty();
    weekId = $(caller).parent().children("h4").attr("val");
    Dajaxice.student.RecordDelete(add_or_update_record_callback,
                                 {'deleteWeekId':weekId});
  }
