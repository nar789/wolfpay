# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm,Join1Form,Join2Form
from .models import Shop,Product
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
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

def button(request,sid,pid):
	p=get_object_or_404(Product.objects.filter(id=pid))
	s=get_object_or_404(Shop.objects.filter(id=sid))
	return render(request,"wolfpay/button.html",{'p':p,'s':s})


def pay(request,sid,pid):
	
	return HttpResponse("pay")