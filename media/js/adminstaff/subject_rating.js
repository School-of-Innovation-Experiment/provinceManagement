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
  $("#review_table").html(data.table);
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
  var changed_grade = $('#id_subject_recommend').find("option:selected").val();
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
