var glo_project_id;
var fund_project_id;
$().ready(function(){
  var strUrl = location.href.split("/");
  fund_project_id =  strUrl[strUrl.length-1];
  // alert(fund_project_id);
})
function get_subject_id(project_id){
  glo_project_id = project_id;
}
function get_review_list(project_id){
  $("#review_table").empty();
  var project_id = project_id;

  Dajaxice.adminStaff.get_subject_review_list(review_list_callback,{'project_id':project_id});
}

function review_list_callback(data){
  $("#review_table").append("<thead><tr><th>评价</th><th>项目选题意义</th><th>科技研究价值</th><th>项目创新之处</th><th>项目可行性</th><th>预期成果</th><th>指导教师科研能力</th></tr><tbody id="+"review_table_body"+"><t></tbody></thead>");
  $.each(data.review_list, function(i, item)
	 {
	   $("#review_table_body").append("<tr>");
	   $.each(item, function(i ,content){
	     $("#review_table_body").append("<td>"+content+"</td>");
	   });
	   $("#review_table_body").append("</tr>");
	 });
}

function subject_grade(){
  var changed_grade = $('#id_subject_grade').find("option:selected").val();

  Dajaxice.adminStaff.change_subject_grade(change_grade_callback,{'project_id':glo_project_id,"changed_grade":changed_grade});
}
function change_grade_callback(data){
  window.location.reload();
}

function change_subject_recommend(){
  var changed_grade = $('#id_subject_grade').find("option:selected").val();
	$("#alert_message").css("display", "none");
  Dajaxice.adminStaff.change_subject_recommend_state(change_recommend_state_callback,{'project_id':glo_project_id,"changed_grade":changed_grade});
}
function change_recommend_state_callback(data){
	if(data.status == "1"){
 		window.location.reload();
	}
	else{
		$("#alert_message").css("display", "block");
	}
}


function release_news(){
  release=true;
  $("#subject_table_body tr").each(function(){
    for (var i = 0; i < 5; ++i){
      if ($(this).find("td").eq(i).text()=="未指定")
	release=false;
    }
  });
  if (release)
  {
    html_str = $("#subject_table")[0].outerHTML;
    Dajaxice.adminStaff.Release_News(release_news_callback, {html: html_str});
    $('#myrelease').modal('show');
  }

  else
  {
    $('#myunrelease').modal('show');

  }

}
function release_news_callback(data){

}
function add_or_update_funds() {
  $("#funds_error_message").empty();  
  Dajaxice.adminStaff.fundsChange(add_or_update_funds_callback,
                                {'form':$('#funds_change_form_info').serialize(true),
                                  'name':$('#name_div').find("option:selected").text(),
                                  //'name':$('#name_div').find("option:selected").val(),
                                'pid':fund_project_id
                                });


}

function add_or_update_funds_callback(data) {

    if(data.status == "2") {
    $.each(data.error_id, function (i, item){
      object = $('#'+item);
      object.css("border-color", 'red');
    });
  }
  else if(data.status == "0") {

    $("#project_funds_table").html(data.table);
  }
  $("#funds_error_message").append("<strong>"+data.message+"</strong>");
}

function delete_funds(caller) {
  $("#funds_error_message").empty();  
  funds_remaining = $(caller).parent().parent().children("td:eq(3)").html();
  Dajaxice.adminStaff.FundsDelete(add_or_update_funds_callback,
                                {'funds_remaining': funds_remaining,
                                'pid':fund_project_id});
}






