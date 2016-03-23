$(function(){

$(document).on("click","a.add",function(){
	var target=$(this).parent().next();
	var len=target.find("tr").length-1;
	var type=$(this).attr("category");
	var str="			<tr>\
				<td><input class=\"error\" name=\"achievements_"+type+"_"+len+"_0\" type=\"text\"></td>\
				<td><input name=\"achievements_"+type+"_"+len+"_1\" type=\"text\"></td>\
				<td><input name=\"achievements_"+type+"_"+len+"_2\" type=\"text\"></td>\
				<td><input name=\"achievements_"+type+"_"+len+"_3\" type=\"text\"></td>\
				<td><a class=\"btn btn-success save\">保存</a></td>\
							</tr>";
	target.append(str);
});

$(document).on("click","a.save",function(){
	var target=$(this).parent().parent();
	var values=new Array();
	var items=target.find("input");
	for(var i=0;i<items.length;i++)
	{
		if(items[i].value=="")
		{
			alert("请输入有效值");
			items[i].
		}
		values[i]=items[i].value;
	}

});

$(document).on("click","a.delete",function(){

});

});