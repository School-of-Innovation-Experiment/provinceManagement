function file_application () {
	alert("jinlaile");
	Dajaxice.student.file_application(file_application_callback,{});
}

function file_application_callback (data) {
	alert(data.message);
}