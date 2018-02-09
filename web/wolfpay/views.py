# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm,Join1Form,Join2Form
from .models import Shop,Product,Transaction
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from .coin import create_address, get_transaction
import datetime
import requests,json
# Create your views here.

def index(request):
	context={'user':request.user}
	return render(request,'wolfpay/index.html',context)


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
			return HttpResponse('login fail');
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
			return HttpResponse("송금요청을 완료했습니다.")				
		else:
			return HttpResponse("유효시간이 만료되었습니다.")
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
			return HttpResponse("결제 내역이 존재하지 않습니다.")
		t=Transaction.objects.filter(name=name,phone=phone)
		s=get_transaction_list(t)
		if len(s)==0:
			return HttpResponse("결제 내역이 존재하지 않습니다.")
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
			return HttpResponse("상품생성이 완료됐습니다.")
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
			return redirect('product')
		else:
			return render(request,"wolfpay/add_product.html",{'update':True,'p':p})
	else:
		return redirect('login')

def delete_product(request,id):
	if request.user.is_authenticated:
		p=get_object_or_404(Product,id=id)
		p.delete()
		return redirect('product')
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
				return HttpResponse("결제 내역이 존재하지 않습니다.")
			return render(request,"wolfpay/get_orders.html",{'s':ft})
		else:
			t=Transaction.objects.filter(sid=s).exclude(name='').order_by('-time')[:5]
			ft=get_transaction_list(t)
			if len(ft)==0:
				return HttpResponse("결제 내역이 존재하지 않습니다.")
			return render(request,"wolfpay/orders.html",{'s':ft})
	else:
		return redirect('login')

def sales(request):
	return HttpResponse("sales")