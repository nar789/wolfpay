from django.conf.urls import include,url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^accounts/logout/$',views.logoutview,name='logout'),
	url(r'^accounts/login/$',views.loginview,name='login'),
	url(r'^accounts/join/$',views.joinview,name='join'),
	url(r'^accounts/',include('django.contrib.auth.urls')),
	url(r'^product/$',views.productview,name='product'),
	url(r'^button/(\d+)/(\d+)/$',views.button,name='button'),
	url(r'^pay/(\d+)/(\d+)/$',views.pay,name='pay'),
]