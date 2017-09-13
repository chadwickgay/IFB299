from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
	return render(request, 'IFB299app/index.html')

def createaccount(request):
	return render(request, 'IFB299app/createaccount.html')

def login(request):
	return render(request, 'IFB299app/login.html')

def register(request):
	return render(request, 'IFB299app/register.html')

def dashboard(request):
	return render(request, 'IFB299app/dashboard.html')

