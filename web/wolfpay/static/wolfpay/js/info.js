function send(){
	var p=$("#price").val();
	var a=$("#btcaddr").val();
	if(!p || !a){
		alert('송금금액과 지갑주소를 입력해주세요.');
		return;
	}
	$.get(sendurl+"?price="+p+"&addr="+a+"&save=True",function(d,s){
		alert(d);
		$("#price").val("");
		$("#btcaddr").val("");
		sendlist();
	});
}

function sendlist(){
	$.get(sendurl+"?save=False",function(d,s){
		$("#sendlist").html(d);
		$("#price").val("");
		$("#btcaddr").val("");
	});	
}