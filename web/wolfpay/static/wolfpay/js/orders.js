var start=5;
function more(url){
	$("#more").html("잠시만 기다려주세요.");
	var token=$('[name="csrfmiddlewaretoken"]').val();
	$.post(url,{'start':start,'csrfmiddlewaretoken':token},function(d,s){
		$("#content").append(d);
		start+=5;
		if(d.length<100)
			$("#more").remove();
		else
			$("#more").html("더보기");
	});
}