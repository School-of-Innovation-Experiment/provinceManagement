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
	Dajaxice.school.Query_Alloced_Expert(Query_Alloced_Expert_callback,{'project_id': glo_project_id});
}
function Query_Alloced_Expert_callback(data){
	$("#alloc_expert_list").html(data.expert_list_html);
}
function save(){
	expert_list = []
	$("input[name='checkbox']:checkbox:checked").each(function(){ 
		expert_list.push($(this).val());
	}) 
	Dajaxice.school.Alloc_Project_to_Expert(Alloc_Project_to_Expert_callback,{'expert_list': expert_list, 'project_id': glo_project_id});
}
function Alloc_Project_to_Expert_callback(data){
	if(data.message == "empty input"){
		alert("空输入");
	}
	else{
		var target_tr = "#tr_" + glo_project_id;
		$(target_tr).children('td').eq(5).html(Join_td_1());
		var add_html = $('<tr id="tr_' + glo_project_id + '">' + $(target_tr).html() + '</tr>');
		$(target_tr).remove();
		$("#alloced_subject_table_body").prepend(add_html);
	}
}
function cancel_this(){
	Dajaxice.school.Cancel_Alloced_Experts(Cancel_Alloced_Experts_callback,{'project_id': glo_project_id});
}

function Cancel_Alloced_Experts_callback(data){
	var target_tr = "#tr_" + glo_project_id;
	$(target_tr).children('td').eq(5).html(Join_td_2());
	var add_html = $('<tr id="tr_' + glo_project_id + '">' + $(target_tr).html() + '</tr>');
	$(target_tr).remove();
	$("#unalloced_subject_table_body").prepend(add_html);
}

function Join_td_1(){
    ret = '<a data-toggle="modal" href="#query_or_cancel" ';
    ret += 'id="allocid_' + glo_project_id + '" onclick="query_or_cancel(' + "'" + glo_project_id + "'" + ');">查询或取消指派</a>';
    return ret;
}
function Join_td_2(){
    ret = '<a data-toggle="modal" href="#alloc_choice" ';
    ret += 'id="allocid_' + glo_project_id + '" onclick="get_subject_id(' + "'" + glo_project_id + "'" + ');">指派专家</a>';
    return ret;
}





