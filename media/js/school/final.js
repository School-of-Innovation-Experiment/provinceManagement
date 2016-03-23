$(function(){

	$(document).on("click","a.add",function(){
		var target=$(this).parent().next();
		var len=target.find("tr").length-1;
		var category=$(this).attr("category");
		var str="			<tr>\
		<td><input category=\"text\" required></td>\
		<td><input category=\"text\" required></td>\
		<td><input category=\"text\" required></td>"
		if(category==3)
		{
			str+="<td><select style=\"margin-top:12px\">\
					  <option value=\"国际级\">国际级</option>\
					  <option value=\"国家级\">国家级</option>\
					  <option value=\"省级\">省级</option>\
					  <option value=\"市级\">市级</option>\
					  <option value=\"校级\">校级</option>\
					</select></td>";
		}
		else
		{
			str+="<td><input category=\"text\" required></td>";
		}
		str+="<td><a class=\"btn btn-success save\" category=\""+category+"\" style=\"margin-top:12px\">保存</a></td></tr>";
		target.append(str);
	});

	$(document).on("click","a.save",function(){
		var path=window.location.pathname;
		var uuid=path.substring(path.lastIndexOf("/")+1);
		var target=$(this).parent().parent();
		var values=new Array();
		var category=$(this).attr("category");
		var items=target.find("input");
		for(var i=0;i<items.length;i++)
		{
			if(items[i].value=="")
			{
				alert("请输入有效值");
				items[i].focus();
				return;
			}
			values[i]=items[i].value;
		}
        if(category==3)
        {
            values[3]=target.find("option:selected").text();
        }
		Dajaxice.school.achievement_save(function(data){
			$("#achievements").html(data);
		},
		{
			'project_id':uuid,
			'values':values,
			'category':category,
		});

	});

	$(document).on("click","a.delete",function(){
 	   var path=window.location.pathname;
	   var uuid=path.substring(path.lastIndexOf("/")+1);
       Dajaxice.school.achievement_delete(function(data){
            $("#achievements").html(data);
        },
        {
            'project_id':uuid,
            'id':$(this).attr("uuid"),
        });

	});

});
