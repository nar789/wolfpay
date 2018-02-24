var op_cnt=1;
var op_confirm_cnt=0;
var op={'data':[]};

function del(idx) {
	if($("#op"+idx)){
		$("#op"+idx).remove();
	}
}

function add(){
	op_cnt++;
	$("#op_container").append("<div id=op"+op_cnt+"><input id=\"op_content"+op_cnt+"\" class=\"form-control op-input\">&nbsp;<b onclick='del("+op_cnt+
		")' class=\"btn btn-danger\"><i class=\"fas fa-trash-alt\"></i></b></div>");
}

function op_save(){
	let title=$("#op_title").val();
	
	op['data'][op_confirm_cnt]={"title":title,"op":[]};
	var cnt=0;
	for(var i=1;i<=op_cnt;i++){
		let content=$("#op_content"+i).val();
		if(content)
			op['data'][op_confirm_cnt]["op"][cnt++]=content;
	}
	
	$("#op_confirm").append("<div id=op_confirm_container"+op_confirm_cnt+">"+"<span class='badge'>"+title+"</span>"
		+" <select id=op_confirm_select"+op_confirm_cnt
		+"></select> <b class='btn btn-danger' onclick='op_confirm_del("+op_confirm_cnt+")'><i class=\"fas fa-trash-alt\"></i></b></div>");
	var cnt=0;
	for(var i=1;i<=op_cnt;i++){
		let content=$("#op_content"+i).val();
		if(content){
			$("#op_confirm_select"+op_confirm_cnt).append("<option value="+cnt+">"+content+"</option");
			cnt++;
		}
	}
	op_confirm_cnt++;
	op_clear();
}

function op_confirm_del(idx){
	$("#op_confirm_container"+idx).remove();
	op['data'][idx]['title']="";
}

function op_clear(){
	$("#op_title").val("");
	for(var i=1;i<=op_cnt;i++)
		del(i);
	op_cnt=0;
	add();
}

function save(){
	var name=$("#name").val();
	var url=$("#url").val();
	var price=$("#price").val();
	if(!name){alert("상품명을 입력해주세요.");return;}
	else if(!url){alert("상품페이지 주소를 입력해주세요.");return;}
	else if(!price){alert("상품가격을 입력해주세요.");return;}
	s={'data':[]}
	for(var i=0;i<op_confirm_cnt;i++){
		let title=op['data'][i]['title'];
		if(title){
			let arr=op['data'][i]['op'];
			s['data'].push({"title":title,"op":arr});
		}
	}
	$("#op").val(JSON.stringify(s));
	//alert(JSON.stringify(s));
	$("#add_prod_form").submit();
}

function insert_option(data){
	try{
		r=JSON.parse(data);
	}catch(e)
	{
		return;
	}

	for(var i=0;i<r['data'].length;i++){
		$("#op_title").val(r['data'][i].title);
		let cnt=r['data'][i].op.length-1;
		for(var j=0;j<cnt;j++){
			add();
		}
		cnt++;
		for(var j=1;j<=cnt;j++){
			$("#op_content"+j).val(r['data'][i].op[j-1]);
		}
		op_save();
	}
}
