var start=5;
function more(url){
	$("#more").html("<button type='button' class='btn btn-success btn-lg btn-block'>잠시만 기다려주세요.</button>");
	var token=$('[name="csrfmiddlewaretoken"]').val();
	$.post(url,{'start':start,'csrfmiddlewaretoken':token},function(d,s){
		if(d.length<100)
			$("#more").html("<div class='alert alert-warning' role='alert'>더 이상 결제 내역이 존재하지 않습니다.</div>");
		else{
			$("#content").append(d);
			start+=5;
			$("#more").html("<button type='button' class='btn btn-success btn-lg btn-block' onclick='more(\""+url+"\")'>더보기</button>");
		}
	});
}