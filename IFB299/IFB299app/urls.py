from django.conf.urls import url
from IFB299app import views

urlpatterns = [
	url(r'^$', views.index, name='index')
]