var glo_project_id;
function get_subject_id(project_id){
  glo_project_id = project_id;
}
function get_review_list(project_id){
  $("#review_table").empty();
  var project_id = project_id;

  Dajaxice.adminStaff.get_subject_review_list(review_list_callback,{'project_id':project_id});
}

function review_list_callback(data){
  $("#review_table").append("<thead><tr><th>评价</th><th>项目选题意义</th><th>科技研究价值</th><th>项目创新之处</th><th>项目可行性</th><th>预期成果</th><th>指导教师科研能力</th><th>总分</th></tr><tbody id="+"review_table_body"+"><t></tbody></thead>");
  $.each(data.review_list, function(i, item)
	 {
	   $("#review_table_body").append("<tr>");
	   $.each(item, function(i ,content){
	     $("#review_table_body").append("<td>"+content+"</td>");
	   });
	   $("#review_table_body").append("</tr>");
	 });
  $("#review_table_body").append("<tr>");
  $("#review_table_body").append("<td>平均</td>");
  $.each(data.average_list, function(i, content){
    $("#review_table_body").append("<td>"+content+"</td>");
  });
  $("#review_table_body").append("</tr>");
}

function subject_grade(){
  var changed_grade = $('#id_subject_grade').find("option:selected").val();

  Dajaxice.adminStaff.change_subject_grade(change_grade_callback,{'project_id':glo_project_id,"changed_grade":changed_grade});
}
function change_grade_callback(data){
	var target = "#gradeid_" + glo_project_id;
	$(target).html(data.res);
}

function change_subject_recommend(){
  var changed_grade = $('#id_subject_grade').find("option:selected").val();
	$("#alert_message").css("display", "none");
  Dajaxice.adminStaff.change_subject_recommend(change_recommend_state_callback,{'project_id':glo_project_id,"changed_grade":changed_grade});
}
function change_recommend_state_callback(data){
	if(data.status == "1"){
		var target = "#gradeid_" + glo_project_id;
 		$(target).html(data.res);
		$("#id_remaining").html("剩余数量:"+data.remaining);
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
    var table = $("#defined_subject_table");
    html_originstr = $("#defined_subject_table")[0].outerHTML;
    $("#defined_subject_table thead tr").each(function(){
      $(this).find("th").eq(4).remove();
    });
    $("#defined_subject_table tbody tr").each(function(){
      $(this).find("td").eq(5).html($(this).find("td").eq(5).find('a').text());
      $(this).find("td").eq(4).remove();
    });

    html_str = $("#defined_subject_table")[0].outerHTML;

    $("#defined_subject_table")[0].innerHTML = html_originstr;
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
