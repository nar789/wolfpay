from django.conf.urls import include,url
from . import views

urlpatterns=[
	url(r'^$',views.index,name='index'),
	url(r'^robots.txt$',views.robots,name='robots'),

	url(r'^accounts/logout/$',views.logoutview,name='logout'),
	url(r'^accounts/login/$',views.loginview,name='login'),
	url(r'^accounts/join/$',views.joinview,name='join'),
	url(r'^accounts/',include('django.contrib.auth.urls')),
	
	url(r'^product/$',views.productview,name='product'),
	url(r'^product/add/$',views.add_product,name='add_product'),
	url(r'^product/update/(\d+)/$',views.update_product,name='update_product'),
	url(r'^product/delete/(\d+)/$',views.delete_product,name='delete_product'),
	url(r'^product/source/(\d+)/$',views.source_product,name='source_product'),	
	
	url(r'^button/(\d+)/$',views.button,name='button'),
	url(r'^pay/(\d+)/$',views.pay,name='pay'),
	url(r'^currency/(\d+)/$',views.currency,name='currency'),
	url(r'^history/$',views.history,name='history'),

	url(r'^orders/$',views.orders,name='orders'),
	
	url(r'^sales/$',views.sales,name='sales'),
	url(r'^get_sales/month$',views.get_sales_month,name='get_sales_month'),
	url(r'^get_sales/year$',views.get_sales_year,name='get_sales_year'),
	url(r'^get_sales/week$',views.get_sales_week,name='get_sales_week'),

	url(r'^info/$',views.info,name='info'),
	url(r'^send/$',views.send,name='send'),
	url(r'^contact/$',views.contact,name='contact'),
	url(r'^intro/$',views.intro,name='intro'),

]