from django.conf.urls import url
from IFB299app import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^createaccount/$', views.createaccount, name='createaccount'),
	url(r'^login/$', views.login, name='login'),
	url(r'^register/$', views.register, name='register'),
	url(r'^dashboard/$', views.dashboard, name='dashboard')
]