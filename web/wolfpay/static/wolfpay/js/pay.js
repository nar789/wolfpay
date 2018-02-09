
var m=3;
var s=0;
function pay(){
	var name=$("#name").val();
	var phone=$("#phone").val();
	var price=$("#price").val();
	var op={};
	op['data']=[];
	for(var i=0;i<p['data'].length;i++){
		var data={};
		data['title']=p['data'][i].title;
		data['op']=[];
		data['op'].push($("#sel"+i).val());
		op['data'].push(data);
	}
	$("#op").val(JSON.stringify(op));
	if(price=="")
		alert("금액이 확정중입니다. 잠시만 기다려 주세요.");
	else if(name=="" || phone=="")
		alert("이름과 핸드폰 번호를 기입해주세요.");
	else
		$("#pay").submit();
}
function showqr(){
	$("#qrcode").qrcode("bitcoin:{{addr}}");
}
function req(){
	$.get(currency_url,function(d,s){
		if(d==0)
			req();
		else{
			$("#price").val(d);
			d=parseFloat(d);
			d=d/Math.pow(10,8);
			$("#btcprice").val(d);
		}
	});
}
function settime(){
	s--;
	if(s==-1)
	{
		s=59;
		m--;
		if(m==-1){
			location.reload();
			return;
		}
	}
	var mt,st;
	mt="0"+m;
	if(s<0)s=0;
	if(s<10)st="0"+s;
	else st=""+s;
	$("#time").html("유효시간 "+mt+":"+st);
}
req();
showqr();
setInterval(function(){settime();},1000);