# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm,Join1Form,Join2Form
from .models import Shop,Product,Transaction,Send
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .coin import create_address, get_transaction
import datetime
import requests,json
from django.db.models import Sum
from django.core.mail import EmailMessage
# Create your views here.

def robots(request):
	return render(request,'wolfpay/robots.txt',{})

def index(request):
	context={'user':request.user,'main':True}
	return render(request,'wolfpay/main.html',context)


def loginview(request):
	if request.method == "POST" :
		form=LoginForm(request.POST)
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('index')
		else:
			return render(request,"wolfpay/complete_product.html",{'msg':'로그인에 실패했습니다.'})
	else:
		form=LoginForm()
		return render(request,"wolfpay/login.html",{'form':form})


def logoutview(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('index')


def joinview(request):
	if request.method=="POST":
		username=request.POST['username']
		email=request.POST['email']
		password=request.POST['password']
		name=request.POST['name']
		addr=request.POST['addr']
		phone=request.POST['phone']
		site=request.POST['site']
		u=User.objects.create_user(username=username,password=password,email=email)
		s=Shop(name=name,addr=addr,phone=phone,site=site,user=u)
		s.save()
		login(request,u)
		return redirect('index')
	else:
		form1=Join1Form()
		form2=Join2Form()
	return render(request,"wolfpay/join.html",{'form1':form1,'form2':form2})


def productview(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		p=Product.objects.filter(sid=s)
		return render(request,"wolfpay/product.html",{'p':p,'s':s})
	else:
		return redirect('login')

def button(request,pid):
	p=get_object_or_404(Product,id=pid)
	s=get_object_or_404(Shop,id=p.sid.id)
	return render(request,"wolfpay/button.html",{'p':p,'s':s})

def pay(request,pid):
	p=get_object_or_404(Product,id=pid)
	s=get_object_or_404(Shop,id=p.sid.id)
	if request.method=="POST":
		tid=request.POST["tid"]
		name=request.POST["name"]
		phone=request.POST["phone"]
		price=request.POST["price"]
		op=request.POST["op"]
		t=get_object_or_404(Transaction,id=tid)
		diff=datetime.datetime.now()
		diff-=t.time
		if diff.seconds<180:
			t.name=name
			t.phone=phone
			t.price=price
			t.op=op
			t.save()
			return render(request,"wolfpay/complete_pay.html",{'msg':'송금요청이 완료되었습니다.'})
		else:
			return render(request,"wolfpay/complete_pay.html",{'msg':'유효시간이 만료되었습니다.'})
	else:
		addr=create_address(s,p)
		t=Transaction(sid=s,pid=p,addr=addr.address,time=datetime.datetime.now())
		t.save()
		return render(request,"wolfpay/pay.html",{
			'tid':t.id,
			'addr':addr.address,
			'price':p.price,
			'op':p.op})
		#render < t.id, addr.address, p.price, time.time() 15분안에 


def currency(request,krw):
	url='https://crix-api-endpoint.upbit.com/v1/crix/candles/lines?code=CRIX.UPBIT.KRW-BTC'
	headers = {'Content-Type': 'application/json; charset=utf-8'}
	r=requests.get(url,headers=headers)
	if r.status_code==requests.codes.ok:
		d=r.json()
		p=d['candles'][0]['tradePrice']
		p=p/pow(10,8)
		p=int(int(krw)/p)
	else:
		p=0
	return HttpResponse("%s" % p)

def history(request):
	s=[]
	if request.method=="POST":
		name=request.POST["name"]
		phone=request.POST["phone"]
		if not name or not phone:
			return render(request,"wolfpay/complete_pay.html",{'msg':'결제 내역이 존재하지 않습니다.'})
		t=Transaction.objects.filter(name=name,phone=phone).order_by('-time')
		s=get_transaction_list(t)
		if len(s)==0:
			return render(request,"wolfpay/complete_pay.html",{'msg':'결제 내역이 존재하지 않습니다.'})
	return render(request,"wolfpay/history.html",{'s':s})

def add_product(request):

	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		if request.method=="POST":
			name=request.POST['name']
			url=request.POST['url']
			price=request.POST['price']
			op=request.POST['op']
			p=Product(name=name,url=url,price=price,op=op,sid=s)
			p.save()
			return render(request,"wolfpay/complete_product.html",{'msg':'상품생성이 완료되었습니다.','callback':'product'})
		else:
			return render(request,"wolfpay/add_product.html",{})
	else:
		return redirect('login')


def update_product(request,id):
	if request.user.is_authenticated:
		p=get_object_or_404(Product,id=id)
		if request.method=="POST":
			name=request.POST['name']
			url=request.POST['url']
			price=request.POST['price']
			op=request.POST['op']
			p.name=name
			p.url=url
			p.price=price
			p.op=op
			p.save()
			return render(request,"wolfpay/complete_product.html",{'msg':'상품수정이 완료되었습니다.','callback':'product'})
		else:
			return render(request,"wolfpay/add_product.html",{'update':True,'p':p})
	else:
		return redirect('login')

def delete_product(request,id):
	if request.user.is_authenticated:
		p=get_object_or_404(Product,id=id)
		p.delete()
		return render(request,"wolfpay/complete_product.html",{'msg':'상품삭제가 완료되었습니다.','callback':'product'})
	else:
		return redirect('login')

def source_product(request,id):
	return render(request,"wolfpay/source_product.html",{'id':id})

def get_transaction_list(t):
	s=[]
	for ti in t:
		txs=get_transaction(ti.addr)
		if len(txs.data)==0:
			status='processing'
			amount='0.0'
		else:
			status=txs.data[0].status
			amount=txs.data[0].amount.amount
		ti.state=status
		ti.receive=float(amount)
		ti.save()
		g={}
		g["addr"]=ti.addr
		g["name"]=ti.pid.name
		if not ti.price:
			ti.price=0
		g["price"]=str(float(ti.price)/pow(10,8))+" BTC";
		g["korprice"]=ti.pid.price
		g["url"]=ti.pid.url
		g["btcprice"]=amount+" BTC"
		g["status"]=status
		g["time"]=ti.time.strftime('%Y-%m-%d %H:%M:%S')
		g["op"]=ti.op
		g["id"]=ti.id
		g["customer"]=ti.name
		g["phone"]=ti.phone
		s.append(g)
	return s

def orders(request):
	if request.user.is_authenticated:
		s=get_object_or_404(Shop,user=request.user)
		if request.method=="POST":
			start=int(request.POST['start'])
			end=start+5;
			t=Transaction.objects.filter(sid=s).exclude(name='').order_by('-time')[start:end]
			ft=get_transaction_list(t)
			if len(ft)==0:
				return render(request,"wolfpay/complete_product.html",{'msg':'결제 내역이 존재하지 않습니다.'})
			return render(request,"wolfpay/get_orders.html",{'s':ft})
		else:
			t=Transaction.objects.filter(sid=s).exclude(name='').order_by('-time')[:5]
			ft=get_transaction_list(t)
			if len(ft)==0:
				return render(request,"wolfpay/complete_product.html",{'msg':'결제 내역이 존재하지 않습니다.'})
			return render(request,"wolfpay/orders.html",{'s':ft})
	else:
		return redirect('login')

def sales(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		total=Transaction.objects.filter(sid=s).aggregate(sum=Sum('receive'))
		return render(request,"wolfpay/sales.html",{'total':total['sum']})
	else:
		return redirect('login')

def get_sales_month(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		year=request.GET['year']
		ret=[]
		for i in range(1,13):
			t=Transaction.objects.filter(sid=s,time__month=i,time__year=year).aggregate(sum=Sum('receive'))
			if t['sum'] is None:
				t['sum']=0.0
			ret.append({'month':str(i),'sum':t['sum']})
		ret=json.dumps(ret)
		return HttpResponse(ret)
	else:
		return redirect('login')

def get_sales_year(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		end=datetime.date.today().year
		start=end-9
		ret=[]
		for i in range(start,end+1):
			t=Transaction.objects.filter(sid=s,time__year=i).aggregate(sum=Sum('receive'))
			if t['sum'] is None:
				t['sum']=0.0
			ret.append({'year':i,'sum':t['sum']})
		ret=json.dumps(ret)
		return HttpResponse(ret)
	else:
		return redirect('login')

def get_sales_week(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		week=request.GET['week']
		week=int(week)
		week*=7
		d=datetime.timedelta(days=week)
		start=datetime.date.today()-d
		ret=[]
		for i in range(0,7):
			start=start+datetime.timedelta(days=1)
			end=start+datetime.timedelta(days=1)
			t=Transaction.objects.filter(sid=s,time__range=[start,end]).aggregate(sum=Sum('receive'))
			if t['sum'] is None:
				t['sum']=0.0
			ret.append({'date':start.strftime('%m/%d'),'sum':t['sum']})
		ret=json.dumps(ret)
		return HttpResponse(ret)
	else:
		return redirect('login')

def info(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)
		if request.method=="POST":
			name=request.POST['name']
			addr=request.POST['addr']
			phone=request.POST['phone']
			site=request.POST['site']
			s.name=name;s.addr=addr;s.phone=phone;s.site=site;
			s.save()
			return render(request,"wolfpay/complete_product.html",{'msg':'수정이 완료되었습니다.'})
		else:
			total=Transaction.objects.filter(sid=s).aggregate(sum=Sum('receive'))
			return render(request,"wolfpay/info.html",{'s':s,'total':total['sum']})
	else:
		return redirect('login')

def send(request):
	if request.user.is_authenticated:
		s=Shop.objects.get(user=request.user)

		if request.GET['save']=="True":
			price=request.GET['price']
			total=Transaction.objects.filter(sid=s).aggregate(sum=Sum('receive'))
			if float(price)>total['sum']:
				return HttpResponse('Warning:보유금액보다 큰 금액을 송금할 수 없습니다.')
			addr=request.GET['addr']
			send=Send(sid=s,price=price,addr=addr,state='처리중',time=datetime.datetime.now())
			send.save()
			return HttpResponse('송금신청이 완료되었습니다.')
		else:
			send=Send.objects.filter(sid=s).order_by("-time")
			for i in send:
				i.time=i.time.strftime("%Y-%m-%d %H:%M:%S")
			return render(request,'wolfpay/send.html',{'send':send})
	else:
		return redirect('login')

def contact(request):
	if request.method=="POST":
		title=request.POST['title']
		detail=request.POST['detail']
		email=request.POST['email']
		mail_title='울프페이::'+email+'님의 문의사항'
		mail_body='title:'+title+'\ndetail:'+detail
		e = EmailMessage(mail_title, mail_body, to=['admin@hume.co.kr'])
		e.send()
		return render(request,"wolfpay/complete_product.html",{'msg':'문의사항이 접수되었습니다.'})
	return render(request,"wolfpay/contact.html",{})

def intro(request):
	return render(request,"wolfpay/complete_product.html",{'msg':'더욱 자세한 서비스소개를 준비중입니다.'})