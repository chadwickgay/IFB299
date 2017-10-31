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
from django.core.exceptions import ObjectDoesNotExist

# render static index/homepage
def index(request):
	return render(request, 'IFB299app/index.html')

@login_required
## Handles logic for primary user dashboard w/ recommendations
def dashboard(request):
    current_user = request.user 
    user_interests = current_user.profile.user_interests
    industry = current_user.profile.industry
    cuisines = current_user.profile.cuisine
    max_price = current_user.profile.max_price
    radius = current_user.profile.radius

    user_liked_location_placeID_set = FeedbackRecommendations.objects.filter(user=current_user)
    place_ID_set_list = []
        
    # extract all liked/disliked locations for user from db
    user_liked_location_placeID_set = FeedbackRecommendations.objects.filter(user=current_user)
    place_ID_set_list = []

    # extract placeIDs from query set 
    for user_liked_location_placeID in user_liked_location_placeID_set:
        place_ID_set_list.append(user_liked_location_placeID.placeID)

    name = []
    slugs = []
    address = []
    rating = []
    photo = []
    place_ID = []

    # loop through users interests to perform Google Places API lookup for each reccomendation
    for interest in user_interests: 
        # URL endpoint for Google Places API
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.4703410197085,153.0250768802915&query="
        
        # URL customisation to allow more specific search for instury & cuisine
        if interest == "Industries" and industry != None:
            url = url + industry
        elif interest == "Restaurants" and cuisines != None:
            url = url + "restaurant%20" + cuisines
        else:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.4703410197085,153.0250768802915&query=" + interest 
        
        ## Add on Parameters
        if max_price != None and interest == ("Restaurants" or "Hotels"):
            url = url + "&maxprice=" + max_price
        if radius != None:
            url = url + "&radius=" + radius
        else: 
            url = url + "&radius=20"
            
        # reset location for each user interest
        # used to cycle thruogh Google API results 
        location = 0;

        if interest == "Industries":
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + industry
        elif interest == "Restaurants" and cuisines != None:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + cuisines
        else:
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&location=-27.470125,153.021072&radius=20&query=" + interest 
        
        # process returned JSON object
        response = requests.get(url) 
        file = response.json() 
        
        # ignore locations user has already provided feedback for 
        for i in range(len(file['results'])): 
            if file['results'][location]['place_id'] in place_ID_set_list: 
                location += 1
                print ("Print found PlaceID")
                print (place_ID_set_list[i])
            else: 
                break 

        # prepare / store information in lists
        place_ID.append(file['results'][location]['place_id'])
        name.append(file['results'][location]['name'])
        address.append(file['results'][location]['formatted_address'])
        try:
            rating.append(file['results'][location]['rating'])
        except KeyError:
            rating.append(None)
        slugs.append(slugify(file['results'][location]['name']))
        
        try:
            photo.append('https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&maxheight=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + (file['results'][location]['photos'][0]['photo_reference']))
        except KeyError:
            photo.append('http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg')

    # handle user feedback with like/dislike buttons
    if request.GET: 
        input_name = request.GET.get("Name", "")
        input_placeID = request.GET.get("PlaceID", "")
        
        if '_like' in request.GET:          
             f = FeedbackRecommendations(name=input_name, placeID = input_placeID, response=True, user=current_user) 
             f.save() 
             print("like")

             return redirect('/IFB299app/dashboard/')
 
        elif '_dislike' in request.GET:  
             f = FeedbackRecommendations(name=input_name, placeID = input_placeID, response=False, user=current_user) 
             f.save() 
             print("dislike")

             return redirect('/IFB299app/dashboard/')

    # zip lists extracted from API (for easier use in template)
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
        try:
            ratings.append(file[i]['result']['rating'])
        except KeyError:
            ratings.append(None)
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
    current_user = request.user 

    # get the place_id based on the name of the location
    place_id = get_place_id(location_name_slug)

    # search for the location using the place_id
    url = "https://maps.googleapis.com/maps/api/place/details/json?placeid=" + place_id + "&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw" 
    response = requests.get(url) 
    file = response.json() 
    
    urlEvents = "https://www.eventbriteapi.com/v3/events/search/?q=" + location_name_slug + "&sort_by=date&token=A3ZOHEB5SAUML5XT5GGK"
    response2 = requests.get(urlEvents) 
    file2 = response2.json() 
    #print(file)

    # store API results for each location in lists
    # note - it is beter to ask for forgiveness than permission in python/django
    # hence, try except used extensively
    context_dict['name'] = file['result']['name'] 
    context_dict['place_id'] = file['result']['place_id'] 
    try:
        context_dict['formatted_address']  = file['result']['formatted_address'] 
    except IndexError:
        pass
    try:
        context_dict['formatted_phone_number']  = file['result']['formatted_phone_number'] 
    except IndexError:
        pass
    try:
        context_dict['rating']  = file['result']['rating'] 
    except IndexError:
        pass
    try:
        context_dict['website']  = file['result']['website']
    except IndexError:
        pass
    try:
        context_dict['price_level']  = file['result']['price_level']
    except IndexError:
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
    except IndexError:
        context_dict['Photo']= 'http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg'
    try:
        context_dict['Photo2']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][1]['photo_reference']
    except IndexError:
        context_dict['Photo2']= 'http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg'
    try:
        context_dict['Photo3']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][2]['photo_reference']
    except IndexError:
        context_dict['Photo3']= 'http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg'
    try:
        context_dict['Photo4']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][3]['photo_reference']
    except IndexError:
        context_dict['Photo4']= 'http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg'
    try:
        context_dict['Photo5']= 'https://maps.googleapis.com/maps/api/place/photo?maxwidth=500&key=AIzaSyBvXpcHlbpL_ESnnNOm07nBCd1LhpZOSzw&photoreference=' + file['result']['photos'][4]['photo_reference']
    except IndexError:
        context_dict['Photo5']= 'http://www.bsmc.net.au/wp-content/uploads/No-image-available.jpg'

    try:
        context_dict['lat'] = file['result']['geometry']['location']['lat']
        context_dict['lng'] = file['result']['geometry']['location']['lng']
    except IndexError:
        pass

    try:
        feedback_made = FeedbackRecommendations.objects.get(placeID = place_id, user=current_user)
        context_dict['feedback_made']  = feedback_made
    except ObjectDoesNotExist:
        print("No feedback made")    


    ## Handle clicking of liked/disliked button (using hidden form elements)
    if request.GET: 
        input_name = request.GET.get("Name", "")
        input_placeID = request.GET.get("PlaceID", "")
    # Handle like/dislike selection
        if '_like' in request.GET:
            f = FeedbackRecommendations(name=input_name, placeID = input_placeID, response=True, user=current_user) 
            f.save() 
            return redirect('/IFB299app/dashboard/')
     
        elif '_dislike' in request.GET: 
            f = FeedbackRecommendations(name=input_name, placeID = input_placeID, response=False, user=current_user) 
            f.save() 

            return redirect('/IFB299app/dashboard/')

    # EVENTS INFORMATION
    # Event One  
    context_dict['Ename'] = file2['events'][0]['name']['text']
    context_dict['Edescription'] = file2['events'][0]['description']['text']
    context_dict['Eurl'] = file2['events'][0]['url']
    # Date and Time Formatting
    startdate= file2['events'][0]['start']['local']
    context_dict['dateS1'] = startdate[:10]
    context_dict['timeS1'] = startdate[11:16]
    enddate = file2['events'][0]['end']['local']
    context_dict['date1'] = enddate[:10]
    context_dict['time1'] = enddate[11:16]
    
    context_dict['Ephoto'] = file2['events'][0]['logo']['original']['url']
    
    #Event Two 
    context_dict['Ename1'] = file2['events'][1]['name']['text']
    context_dict['Edescription1'] = file2['events'][1]['description']['text']
    context_dict['Eurl1'] = file2['events'][1]['url']
    # Date and Time Formatting
    startdate= file2['events'][1]['start']['local']
    context_dict['dateS2'] = startdate[:10]
    context_dict['timeS2'] = startdate[11:16]
    enddate = file2['events'][1]['end']['local']
    context_dict['date2'] = enddate[:10]
    context_dict['time2'] = enddate[11:16]

    context_dict['Ephoto1'] = file2['events'][1]['logo']['original']['url']
    
    # render page   
    return render(request, 'IFB299app/location.html', context_dict)


# handle user registeration / user creation
# uses in built django authentication
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

# handle user interest collection (to form basis of recommendations)
# uses extension of django auth user via profile model
def interests(request):
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
    return render(request, 'IFB299app/interests.html', {
        'profile_form': profile_form,
        })



