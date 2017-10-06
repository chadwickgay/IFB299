from django.shortcuts import render
from django.http import HttpResponse
from .forms import RegisterForm, ProfileForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
import requests
from django.contrib.auth.decorators import login_required
from IFB299app.models import Location, Questions
from django.contrib.contenttypes.models import ContentType
from django.views.generic import FormView 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.utils import timezone
from .forms import RegisterForm, ProfileForm, QuestionsForm


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
    if not request.user.is_staff or not request.user.is_superuser:
        form = QuestionsForm(request.POST or None)
        if form.is_valid() and request.user.is_authenticated():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get("content")
            
            Questions = instance.Questions

    return render(request, 'IFB299app/questions.html', {'Questions_form': form})


def location_list(request):
	today = timezone.now().date()
	queryset_list = Questions.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Questions.objects.all()
	
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
				Q(title__icontains=query)|
				Q(content__icontains=query)|
				Q(user__first_name__icontains=query) |
				Q(user__last_name__icontains=query)
				).distinct()
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)


	context = {
		"object_list": queryset, 
		"title": "List",
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "IFB299app/questions.html", context)

def vote(request):
   thread_id = int(request.POST.get('id'))
   vote_type = request.POST.get('type')
   vote_action = request.POST.get('action')

   thread = get_object_or_404(Thread, pk=thread_id)

   thisUserUpVote = thread.userUpVotes.filter(id = request.user.id).count()
   thisUserDownVote = thread.userDownVotes.filter(id = request.user.id).count()

   if (vote_action == 'vote'):
      if (thisUserUpVote == 0) and (thisUserDownVote == 0):
         if (vote_type == 'up'):
            thread.userUpVotes.add(request.user)
         elif (vote_type == 'down'):
            thread.userDownVotes.add(request.user)
         else:
            return HttpResponse('error-unknown vote type')
      else:
         return HttpResponse('error - already voted', thisUserUpVote, thisUserDownVote)
   elif (vote_action == 'recall-vote'):
      if (vote_type == 'up') and (thisUserUpVote == 1):
         thread.userUpVotes.remove(request.user)
      elif (vote_type == 'down') and (thisUserDownVote ==1):
         thread.userDownVotes.remove(request.user)
      else:
         return HttpResponse('error - unknown vote type or no vote to recall')
   else:
      return HttpResponse('error - bad action')


   num_votes = thread.userUpVotes.count() - thread.userDownVotes.count()

   return HttpResponse(num_votes)
