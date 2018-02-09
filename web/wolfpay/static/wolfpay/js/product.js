var p="";
function show_option(str,id) {
	try{
		p=JSON.parse(str);
	}catch(e){$("#op"+id).html("No option."); return; }
	var op="";
	if(p['data'].length==0)
	{
		$("#op"+id).html("No option.");	
		return;
	}
	for(var i=0;i<p['data'].length;i++)
	{
		op+=p['data'][i].title+"<select id=sel"+i+">";
		for(var j=0;j<p['data'][i].op.length;j++){
			op+="<option id=option"+j+">"+p['data'][i].op[j]+"</option>";
		}
		op+="</select>&nbsp;&nbsp;";
	}
	$("#op"+id).html(op);
}