from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from IFB299app.models import Location, User, FeedbackRecommendations
from django.utils.text import slugify
import json as simplejson

# Create your views here.
def index(request):
	return render(request, 'IFB299app/index.html')


def createaccount(request):
	return render(request, 'IFB299app/createaccount.html')


def login_view(request):
	return render(request, 'IFB299app/login.html')

@login_required
def dashboard(request):
    current_user = request.user 
    user_interests = current_user.profile.user_interests
    industry = current_user.profile.industry
    cuisines = current_user.profile.cuisine

     
    name = []
    slugs = []
    address = []
    rating = []
    photo = []
    place_ID = []

    for interest in user_interests: 
        if interest == "Industries":
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + industry
        elif interest == "Restaurants" and cuisines != None:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + cuisines


        else:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + interest 
        response = requests.get(url) 
        file = response.json() 
        place_ID.append(file['results'][0]['place_id'])
        name.append(file['results'][0]['name'])
        address.append(file['results'][0]['formatted_address'])
        try:
            rating.append(file['results'][0]['rating'])
        except KeyError:
            rating.append(None)
        slugs.append(slugify(file['results'][0]['name']))
        
        try:
            photo.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&maxheight=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + (file['results'][0]['photos'][0]['photo_reference']))
        except KeyError:
            photo.append('../../static/img/No-image-available.jpg')

 
    if request.POST: 
        if '_like' in request.POST: 
             print("like") 
 
             f = FeedbackRecommendations(name="TestTrue", response=True, user=current_user) 
             f.save() 
 
        elif '_dislike' in request.POST: 
             print("dislike") 
 
             f = FeedbackRecommendations(name="TestFalse", response=False, user=current_user) 
             f.save() 

    context_dict = { }
    context_dict ['recommendation_data'] = zip(name, address, rating, place_ID, user_interests, slugs, photo)

    return render(request, 'IFB299app/dashboard.html', context_dict)


def get_place_id(location_name):
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + location_name
    response = requests.get(url) 
    file = response.json() 

    place_id = file['results'][0]['place_id'] 
    #print(place_id)
    return place_id

@login_required
def likedlocations(request):   
    # pull saved placeIDs form the db
    placeID_list = FeedbackRecommendations.objects.filter(user=request.user)

    # lists to store API information
    file = []
    names = []
    addresses = []
    location_types = []
    ratings = []
    slugs = []
    lats = []
    lngs = []

    # get the API results for each of the placeIDs
    for placeID in placeID_list:

        # search for the location using the place_id
        url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + placeID.placeID + "&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw" 
        response = requests.get(url) 
        file.append(response.json())

    # store API results for each location in lists
    for i in range(len(placeID_list)):
        names.append(file[i]['result']['name'])
        slugs.append(slugify(file[i]['result']['name']))
        addresses.append(file[i]['result']['formatted_address'])
        location_types.append(file[i]['result']['types'][0])
        ratings.append(file[i]['result']['rating'])
        lats.append(file[i]['result']['geometry']['location']['lat'])
        lngs.append(file[i]['result']['geometry']['location']['lng'])

    # zip location data for map to pass to template
    json_list = simplejson.dumps(zip(names, lats, lngs))
    
    # zip lists to pass into the context_dict
    context = {}
    context['location_data'] = zip(names, slugs, addresses, location_types, ratings)
    context['json_list'] = json_list
    
    # render page with context_dict
    return render(request, 'IFB299app/likedlocations.html', context)

@login_required
def editprofile(request):
	return render(request, 'IFB299app/editprofile.html')
    

@login_required
def location(request, location_name_slug):
    context_dict = {}

    # get the place_id based on the name of the location
    place_id = get_place_id(location_name_slug)

    # search for the location using the place_id
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw" 
    response = requests.get(url) 
    file = response.json() 

    # store API results for each location in lists
    # note - it is beter to ask for forgiveness than permission in python/django
    # hence, try except used extensively
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
    except KeyError:
        context_dict['Photo']= '../../static/img/No-image-available.jpg'
    try:
        context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
    except KeyError:
        context_dict['Photo2']= '../../static/img/No-image-available.jpg'
    try:
        context_dict['Photo3']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][2]['photo_reference']
    except KeyError:
        context_dict['Photo3']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
    try:
        context_dict['Photo4']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][3]['photo_reference']
    except KeyError:
        context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
    try:
        context_dict['Photo5']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][4]['photo_reference']
    except KeyError:
        context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']

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
        if form.is_valid():
            new_user = form.save()

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/IFB299app/register2/')
    else:
        form = RegisterForm()
    return render(request, 'IFB299app/register.html', {
        'form': form,
        })

def register2(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit=False)

            if profile.user_id is None:
                profile.user_id = request.user

            profile_form.save()
            return redirect('/IFB299app/dashboard/')
    else:
        profile_form = ProfileForm()
    return render(request, 'IFB299app/register2.html', {
        'profile_form': profile_form,
        })



