var fund_project_id;
$().ready(function(){
  var strUrl = location.href.split("/");
  fund_project_id =  strUrl[strUrl.length-1];
  $("#add_funds_record").click(function(){
  $("#funds_error_message").empty();
  Dajaxice.adminStaff.fundsChange(add_or_update_funds_callback,
                                {'form':$('#funds_change_form_info').serialize(true),
                                 'name':$('#name_div').find("option:selected").text(),
                                  //'name':$('#name_div').find("option:selected").val(),
                                 'pid':fund_project_id});
  return false;
  })
  $('#project_funds_table').on("click","button",function(){
     $("#funds_error_message").empty();
     delete_id = $(this).parents('tr').children("td:eq(0)").attr('id');
     Dajaxice.adminStaff.FundsDelete(add_or_update_funds_callback,
                                   {'delete_id': delete_id,
                                    'pid':fund_project_id});
  })
})

function add_or_update_funds_callback(data) {
    if(data. status == "2") {
      $.each(data.error_id, function (i, item){
        object = $('#'+item);
        object.css("border-color", 'red');
      });
    }
    else if(data.status == "0") {
      $("#project_funds_table").html(data.table);
      $("#funds_project_detail").find("#funds_total").html("经费总额: "+data.funds_total);
      $("#funds_project_detail").find("#funds_remain").html("经费余额: "+data.funds_remain);
    }
    $("#funds_error_message").append("<strong>"+data.message+"</strong>");
  }
