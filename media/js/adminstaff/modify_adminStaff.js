function save_adminStaff_info(){
  $("#adminStaff_info_error_message").empty();
  Dajaxice.adminStaff.SaveAdminStaffInfo(SaveAdminStaffInfo_callback,{'form':$('#adminStaff_info_form').serialize(true)});
};
function SaveAdminStaffInfo_callback(data){
	if(data.status == "1"){
		$.each(data.field,function(i,item){
				object = $('#'+item);
				object.css("background","white");
				});
		$("#adminStaff_info_error_message").append("<strong>" + data.message + "</strong>");
		alert("保存成功");
	}
	else
	{
		$.each(data.field,function(i,item){
			object = $('#'+item);
			object.css("background","white");
		});
		//error field background turn into red
		$.each(data.error_id,function(i,item){
			object = $('#'+item);
			object.css("background","red");
		});
		$("#adminStaff_info_error_message").append("<strong>" + data.message + "</strong>");	
	}
}


function save_school_name(){
  // alert($('#school_name_form').serialize(true))

  Dajaxice.adminStaff.SaveSchoolName(SaveSchoolName_callback,{'form':$('#school_name_form').serialize(true)});
};
function SaveSchoolName_callback(data){
	if(data.status == "1")
	{
		$("#info_schoolname").html(data.table);
		alert(data.message)
	}
	else if(data.status == "2")
	{
		alert(data.message)
	}
	else 
	{
		alert(data.message)
	}
}

function delete_school_name(){

  // alert("345345345");
  var deleted_school_name=new Array();
  var j = 0;
  var checkBoxs = $("input[name='_selected_action']:checked");//取得input标签的对象
  for(var i=0; i<checkBoxs.length&&checkBoxs.length>0; i++)
  {
      deleted_school_name[j]=checkBoxs[i].value;
      j++;
  }

  Dajaxice.adminStaff.DeleteSchoolName(DeleteSchoolName_callback,{"deleted_school_name":deleted_school_name});


  // Dajaxice.adminStaff.DeleteSchoolName(DeleteSchoolName_callback);
};





function DeleteSchoolName_callback(data){
	if(data.status == "1")
	{
		alert(data.message);
		$("#info_schoolname").html(data.table);
	}
	else
	{
		alert("删除失败"+data.message);
		$("#info_schoolname").html(data.table);
	}
}



         
function save_major_name(){
  // alert($('#major_name_form').serialize(true))
  Dajaxice.adminStaff.SaveMajorName(SaveMajorName_callback,{'form':$('#major_name_form').serialize(true)});
};
function SaveMajorName_callback(data){
	if(data.status == "1")
	{
		$("#info_majorname").html(data.table);
		alert(data.message)
	}
	else if(data.status == "2")
	{
		alert(data.message)
	}
	else 
	{
		alert(data.message)
	}
}

function delete_major_name(){

  // alert("345345345");
  var deleted_major_name=new Array();
  var j = 0;
  var checkBoxs = $("input[name='_selected_action']:checked");//取得input标签的对象

  // alert(checkBoxs);
  for(var i=0; i<checkBoxs.length&&checkBoxs.length>0; i++)
  {
      deleted_major_name[j]=checkBoxs[i].value;
      j++;
  }
  // alert("sbsbsb");
  // alert(deleted_major_name);

  Dajaxice.adminStaff.DeleteMajorName(DeleteMajorName_callback,{"deleted_major_name":deleted_major_name});


  // Dajaxice.adminStaff.DeleteSchoolName(DeleteSchoolName_callback);
};





function DeleteMajorName_callback(data){
	if(data.status == "1")
	{
		alert(data.message);
		$("#info_majorname").html(data.table);
	}
	else
	{
		alert("删除失败"+data.message);
		$("#info_majorname").html(data.table);
	}
}
