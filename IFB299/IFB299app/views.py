from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, ProfileForm, QuestionsForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from IFB299app.models import Location, Questions

# Create your views here.
def index(request):
	return render(request, 'IFB299app/index.html')


def createaccount(request):
	return render(request, 'IFB299app/createaccount.html')


def login_view(request):
	return render(request, 'IFB299app/login.html')

@login_required
def dashboard(request):
    location_list = Location.objects.all
    context_dict = {'locations': location_list}
    return render(request, 'IFB299app/dashboard.html', context_dict)


def get_place_id(location_name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + location_name
    response = requests.get(url) 
    file = response.json() 

    place_id = file['results'][0]['place_id'] 
    #print(place_id)
    return place_id

def savedlocations(request):
	return render(request, 'IFB299app/savedlocations.html')

def editprofile(request):
	return render(request, 'IFB299app/editprofile.html')
    

@login_required
def location(request, location_name_slug):
    context_dict = {}

    #Get the place_id based on the name of the location
    place_id = get_place_id(location_name_slug)


    #Search for the location using the place_id
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw" 
    response = requests.get(url) 
    file = response.json() 
    
    #print(file)

    context_dict['name'] = file['result']['name'] 
    context_dict['place_id'] = file['result']['place_id'] 
    try:
        context_dict['formatted_address']  = file['result']['formatted_address'] 
    except KeyError:
        pass
    try:
        context_dict['formatted_phone_number']  = file['result']['formatted_phone_number'] 
    except KeyError:
        pass
    try:
        context_dict['rating']  = file['result']['rating'] 
    except KeyError:
        pass
    try:
        context_dict['website']  = file['result']['website']
    except KeyError:
        pass
    try:
        context_dict['price_level']  = file['result']['price_level']
    except KeyError:
        pass
    try:
        context_dict['Monday'] = file['result']['opening_hours']['weekday_text'][0]
        context_dict['Tuesday'] = file['result']['opening_hours']['weekday_text'][1]
        context_dict['Wednesday'] = file['result']['opening_hours']['weekday_text'][2]
        context_dict['Thursday'] = file['result']['opening_hours']['weekday_text'][3]
        context_dict['Friday'] = file['result']['opening_hours']['weekday_text'][4]
        context_dict['Saturday'] = file['result']['opening_hours']['weekday_text'][5]
        context_dict['Sunday'] = file['result']['opening_hours']['weekday_text'][6]
    except KeyError:
        pass
    try:
        context_dict['Photo']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&maxheight=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][0]['photo_reference']
        context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
        context_dict['Photo3']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][2]['photo_reference']
        context_dict['Photo4']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][3]['photo_reference']
        context_dict['Photo5']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][4]['photo_reference']
    except KeyError:
        pass

    try:
        context_dict['lat'] = file['result']['geometry']['location']['lat']
        context_dict['lng'] = file['result']['geometry']['location']['lng']
    except KeyError:
        pass
    
    return render(request, 'IFB299app/location.html', context_dict)

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

def add_question(request):
    
    form = QuestionsForm(request.POST or None)
    if form.is_valid():
       print(request.POST)
    
    return render(request, 'IFB299app/location.html', {'form': form_class,})