var label=[];
var data=[];
var yearurl="";
var monthurl="";
var weekurl="";
var chart;
var w=0;

function menu(type) {
	$("#submenu").html("");
	if(type==1){
		year();
	}else if(type==2){
		month();
	}else if(type==3){
		week();
	}
}

function dateformat(date){
	return date.getFullYear()+"년"+(date.getMonth()+1)+"월"+date.getDate()+"일";
}
function week(){
	var end=new Date();
	end.setDate(end.getDate()-(7*w));
	var start=new Date();
	start.setDate(start.getDate()-(7*w)-6);
	var s="";
	s+="<button class='btn btn-primary' onclick='prev()'><<</button>&nbsp;";
	s+="<p class=submenu-text2>";
	s+=dateformat(start)+" ~ "+dateformat(end);
	s+="</p>";
	s+="&nbsp;<button class='btn btn-primary' onclick='next()'>>></button>";
	$("#submenu").html(s);
	$.get(weekurl+"?week="+(w+1),function(d,s){
		o=JSON.parse(d);
		data=[];
		label=[];
		for(var i=0;i<o.length;i++){
			label.push(o[i].date);
			data.push(o[i].sum);
		}
		chart.data.datasets[0].data=data;
		chart.data.labels=label;
		chart.update();
	});
}
function next() {
	if(w==0)return;
	w--;
	week();
}
function prev(){
	w++;
	week();
}

function month(){
	var sel="<h5 class=submenu-text>년도</h5>&nbsp;<select id=sel>";
	var y=new Date().getFullYear();
	var b=y-9;
	for(var i=y;i>=b;i--){
		sel+="<option>"+i+"</option>";
	}
	sel+="</select>&nbsp;<button class='btn btn-primary' onclick='get_month()'>검색</button>";
	$("#submenu").html(sel);
	get_month();
}	
function get_month(){
	var y=$("#sel").val();
	$.get(monthurl+"?year="+y,function(d,s){
		o=JSON.parse(d);
		data=[];
		label=[];
		for(var i=0;i<o.length;i++){
			label.push(o[i].month+'월');
			data.push(o[i].sum);
		}
		chart.data.datasets[0].data=data;
		chart.data.labels=label;
		chart.update();
	});
}

function SetWeekUrl(url){
	weekurl=url;
}

function SetMonthUrl(url){
	monthurl=url;
}

function SetYearUrl(url){
	yearurl=url;
}
function year(){
	var y=new Date().getFullYear();
	var b=y-9;
	label=[];
	for(var i=b;i<=y;i++){
		str=i+"년";
		label.push(str);
	}
	$.get(yearurl,function(d,s){
		o=JSON.parse(d);
		data=[];

		for(var i=0;i<o.length;i++)
			data.push(o[i].sum);
		chart.data.datasets[0].data=data;
		chart.data.labels=label;
		chart.update();
	});
	
}

function init(){
	var ctx = document.getElementById("myChart").getContext('2d');
	chart = new Chart(ctx, {
	    type: 'bar',
	    data: {
	        labels: ["wolfpay", "wolfpay", "wolfpay", "wolfpay", "wolfpay", "wolfpay"],
	        datasets: [{
	            label: '매출',
	            data: [10, 10, 10, 10, 10, 10],
	            backgroundColor: [
	                'rgba(255, 99, 132, 0.2)',
	                'rgba(54, 162, 235, 0.2)',
	                'rgba(255, 206, 86, 0.2)',
	                'rgba(75, 192, 192, 0.2)',
	                'rgba(153, 102, 255, 0.2)',
	                'rgba(255, 159, 64, 0.2)'
	            ],
	            borderColor: [
	                'rgba(255,99,132,1)',
	                'rgba(54, 162, 235, 1)',
	                'rgba(255, 206, 86, 1)',
	                'rgba(75, 192, 192, 1)',
	                'rgba(153, 102, 255, 1)',
	                'rgba(255, 159, 64, 1)'
	            ],
	            borderWidth: 1
	        }]
	    },
	    options: {
	        scales: {
	            yAxes: [{
	                ticks: {
	                    beginAtZero:true
	                }
	            }]
	        }
	    }
	});
}
window.onload=init();