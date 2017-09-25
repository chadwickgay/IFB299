from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

# Create your views here.
def index(request):
	return render(request, 'IFB299app/index.html')

def createaccount(request):
	return render(request, 'IFB299app/createaccount.html')

def login_view(request):
	return render(request, 'IFB299app/login.html')

def dashboard(request):
	return render(request, 'IFB299app/dashboard.html')

def location(request):
    return render(request, 'IFB299app/location.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/IFB299app/dashboard/')
    else:
        form = RegisterForm()
    return render(request, 'IFB299app/register.html', {'form': form})

