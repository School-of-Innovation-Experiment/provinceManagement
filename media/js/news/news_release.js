function news_form_submit(){
  var news_content = $("<input>").attr("type", "text").attr("name", "news_content").val($("#editor").html());
  $('#news_form').append($(news_content));
}
$(function (){
  $("#news_form").submit(news_form_submit);
});
