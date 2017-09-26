from django.shortcuts import render
from django.http import HttpResponse
from forms import RegisterForm, ProfileForm
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
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save()
            profile = profile_form.save(commit=False)
            
            if profile.user_id is None:
                profile.user_id = new_user.id

            profile_form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/IFB299app/dashboard/')
    else:
        form = RegisterForm()
        profile_form = ProfileForm()
    return render(request, 'IFB299app/register.html', {
        'form': form,
        'profile_form': profile_form
        })

