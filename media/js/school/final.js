$(function(){
	$(document).on("click","a.add",function(){
		if($(this).hasClass("disabled"))
		{
			alert("编辑权限锁定!");
			return;
		}
		var target=$(this).parent().next();
		var len=target.find("tr").length-1;
		var category=$(this).attr("category");
		var str="			<tr>\
		<td><input type=\"text\"></td>\
		<td><input type=\"text\"></td>"
		if(category==3)
		{
			str+="<td><input type=\"text\"></td>\
			<td><select style=\"margin-top:12px\">\
			<option value=\"国际级\">国际级</option>\
			<option value=\"国家级\">国家级</option>\
			<option value=\"省级\">省级</option>\
			<option value=\"市级\">市级</option>\
			<option value=\"校级\">校级</option>\
			</select></td>";
		}
		else
		{
			str+="<td><input type=\"text\" placeholder=\"请按格式输入时间:如20160101\"></td>\
			<td><input type=\"text\"></td>";
		}
		str+="<td><a class=\"btn btn-success save\" category=\""+category+"\" style=\"margin-top:12px\">保存</a></td></tr>";
		target.append(str);
	});

	$(document).on("click","a.save",function(){
		if($(this).hasClass("disabled"))
		{
			alert("编辑权限锁定!");
			return;
		}
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
		else
		{
			var reg = new RegExp("^[0-9]*$");
			if(values[2].length!=8||!(reg.test(values[2])))
			{
				alert("请输入有效日期");
				items[2].focus();
				return;
			}
		}
		Dajaxice.school.achievement_save(function(data){
			if(data!="readonly")
			{
				$("#achievements").html(data);
			}
			else
			{
				alert("编辑权限锁定!");
			}
		},
		{
			'project_id':uuid,
			'values':values,
			'category':category,
		});

	});

	$(document).on("click","a.delete",function(){
		if($(this).hasClass("disabled"))
		{
			alert("编辑权限锁定!");
			return;
		}
		if(!confirm("确认删除?"))
		{
			return;
		}
		var path=window.location.pathname;
		var uuid=path.substring(path.lastIndexOf("/")+1);
		Dajaxice.school.achievement_delete(function(data){
			if(data!="readonly")
			{
				$("#achievements").html(data);
			}
			else
			{
				alert("编辑权限锁定!");
			}
		},
		{
			'project_id':uuid,
			'id':$(this).attr("uuid"),
		});
	});
});
