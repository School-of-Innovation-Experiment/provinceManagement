var glo_project_id;
var glo_page;
var glo_schoolname;
function get_subject_id(project_id,subject_page,school_name){
  glo_project_id = project_id;
  glo_page = subject_page;
  glo_schoolname = school_name;
}
function get_review_list(project_id){
  $("#review_table").empty();
  var project_id = project_id;

  //Dajaxice.adminStaff.get_subject_review_list(review_list_callback,{'project_id':project_id});
  Dajaxice.adminStaff.get_subject_review_pass_p_list(review_list_pass_p_callback,{'project_id':project_id});
}

function review_list_pass_p_callback(data){
  $("#review_table").append("<thead><tr><th>是否通过审核</th><tbody id="+"review_table_body"+"><t></tbody></thead>");
  $.each(data.review_list, function(i, item)
	 {
	   $("#review_table_body").append("<tr>");
	   $.each(item, function(i ,content){
	     $("#review_table_body").append("<td>"+content+"</td>");
	   });
	   $("#review_table_body").append("</tr>");
	 });
}

function review_list_callback(data){
  $("#review_table").append("<thead><tr><th>项目评价</th><th>创新性得分</th><th>实用性得分</th><th>趣味性得分</th><tbody id="+"review_table_body"+"><t></tbody></thead>");
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
  Dajaxice.adminStaff.change_subject_grade(change_grade_callback,{'project_id':glo_project_id,"changed_grade":changed_grade,"page":glo_page,"school_name":glo_schoolname});
}
function change_grade_callback(data){
  $("#subjectrating_table").html(data.table);
}

function release_news(){
  $('#releaseprogress').modal('show');
  Dajaxice.adminStaff.Release_News(release_news_callback);
}
function release_news_callback(data){

  $('#releaseprogress').modal('hide');
  if (data.release)
   {
     $('#myrelease').modal('show');
   }
  else
  {
    $('#myunrelease').modal('show');

  }

}
