function get_review_list(project_id){
	$("#review_table").empty()
	var project_id = project_id
	
	Dajaxice.adminStaff.get_subject_review_list(review_list_callback,{'project_id':project_id});
	}
	
function review_list_callback(data){
	$("#review_table").append("<thead><tr><th>项目得分</th><th>项目评价</th><tbody id="+"review_table_body"+"><t></tbody></thead>")
		$.each(data.review_list, function(i, item)
		{
			$("#review_table_body").append("<tr>")
			$.each(item, function(i ,content){
				$("#review_table_body").append("<td>"+content+"</td>")
			});
			$("#review_table_body").append("</tr>")
		});
	}
	
function subject_grade(project_id){
	var changed_grade = $('#id_subject_grade').find("option:selected").val()
	
	Dajaxice.adminStaff.change_subject_grade(change_grade_callback,{'project_id':project_id,"changed_grade":changed_grade});
	}	
function change_grade_callback(data){
	
	}