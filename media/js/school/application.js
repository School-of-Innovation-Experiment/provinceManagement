$().ready(function(){
  var div_edit;
  var edit = $('#Richtext_edit').find('#editor');
  $('.richtext_div').on("click",function(){
    div_edit = this;
    $(edit).html($(this).html());
    $('#Richtext_edit').modal('show');
  })
  $('#Richtext_edit').on('hide',function(){
    $(div_edit).html($(edit).html());
  })
})

function form_application_submit(){
  $('.richtext_div').each(function(){
    var div_id = $(this).attr('id');
    var application_content = $("<input>").attr("type", "text").attr("name", div_id).val($(this).html());
    $('#form_application').append($(application_content));
  })

}
$(function (){
  $("#form_application").submit(form_application_submit);
});
