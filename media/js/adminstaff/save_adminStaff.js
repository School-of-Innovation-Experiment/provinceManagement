function save_adminStaff_info(){
  // $("#expert_email_error_message").empty();
  Dajaxice.adminStaff.SaveAdminStaffInfo(SaveAdminStaffInfo_callback,{'form':$('#adminStaff_info_form').serialize(true)});
};
function SaveAdminStaffInfo_callback(data){
  // if (data.status == "1"){
  //   // if success all field background turn into white
  //   $.each(data.field,function(i,item){
  //     object = $('#'+item);
  //     object.css("background","white");
  //     $("#send_mail_table").html(data.table);
  //   });
  //   //$("#time_settings_form").css("background","white");
  //   $("#expert_email_error_message").append("<strong>"+data.message+"</strong>");
  // }
  // else
  // {
  //   $.each(data.field,function(i,item){
  //     object = $('#'+item);
  //     object.css("background","white");
  //   });
  //   //error field background turn into red
  //   $.each(data.error_id,function(i,item){
  //     object = $('#'+item);
  //     object.css("background","red");
  //   });
  //   $("#expert_email_error_message").append("<strong>"+data.message+"</strong>");
  // }
  // $("#close_is_dispatching").trigger('click');
}


function save_school_name(){
  Dajaxice.adminStaff.SaveSchoolName(SaveSchoolName_callback,{'form':$('#school_name_form').serialize(true)});
};
function SaveSchoolName_callback(data){
}
         
function save_major_name(){
  Dajaxice.adminStaff.SaveMajorName(SaveMajorName_callback,{'form':$('#major_name_form').serialize(true)});
};
function SaveMajorName_callback(data){
}
