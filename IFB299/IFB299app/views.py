from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from .forms import UserForm

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



class UserFormView(View):
form_class = UserForm
template_name = 'registration.html'

def get(self, request):
form = self.form_class(none)
return render(request, self.template_name, {'form': form})

def post (self, request):
form = self.form_class(request.POST)

if form.is_valid();

user = form.save(commit = False)
firstname = form.cleaned_data['firstname']
lastname = form.cleaned_data['lastname']
email = form.cleaned_data['email']
password = form.cleaned_data['password']

user.set_password(password)
user.save()

user = authenticate(email = email, password = password)


if user is not None:
if user.is_active:
login(request, user)
return redirect('')# dashboard

return render(request, self.template_name, {'form': form})
