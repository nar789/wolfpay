# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Shop(models.Model):
	name=models.CharField(max_length=200)
	addr=models.CharField(max_length=200)
	phone=models.CharField(max_length=200)
	site=models.CharField(max_length=200)
	user=models.OneToOneField(User,on_delete=models.CASCADE)

	def __str__(self):
		return self.name

class Product(models.Model):
	sid=models.ForeignKey('Shop',on_delete=models.CASCADE)
	name=models.CharField(max_length=200)
	url=models.CharField(max_length=255)
	price=models.IntegerField(null=True)
	op=models.TextField()
	
	def __str__(self):
		return self.name

class Transaction(models.Model):
	sid=models.ForeignKey('Shop',on_delete=models.CASCADE)
	pid=models.ForeignKey('Product',on_delete=models.CASCADE)
	state=models.CharField(max_length=255)
	addr=models.CharField(max_length=255)
	name=models.CharField(max_length=255)
	phone=models.CharField(max_length=255)
	op=models.TextField()
	time=models.DateTimeField(auto_now_add=True,blank=True)
	price=models.IntegerField(null=True)
	receive=models.FloatField(null=True)

	def __str__(self):
		return "%s#%s" %(self.sid.id,self.pid.id)