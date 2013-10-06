var glo_project_id;

function get_subject_id(project_id){
	glo_project_id = project_id;
	clear_check_box();	
}

function clear_check_box(){
	$("[name='checkbox']").removeAttr("checked");
}

function query_or_cancel(project_id){
	glo_project_id = project_id;
	//TODO (ajax) get the expert list from db
	$("#alloc_expert_list").html("hehe");
}

function cancel_this(){
	//TODO (ajax) cancel the re_expert_project related with this project in db
	alert("Hello World");
}





