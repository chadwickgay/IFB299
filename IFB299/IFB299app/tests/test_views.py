
from django.test import TestCase
from IFB299app.models import (Location, User, Profile, Category, FeedbackRecommendations, Country, Region, City, Event)
from model_mommy import mommy
from model_mommy.recipe import (Recipe, foreign_key)
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.test.client import Client
from IFB299app.forms import LoginForm, RegisterForm, ProfileForm

class Modelcoverage(TestCase):
    def setUp (self):
        self.client = Client()
#        """Setting up all the tests"""
#
#        self.attraction_category = Recipe (
#        Category,
#        name="attraction",
#        )
#        
#        self.gen_user = Recipe (
#        User, 
#        first_name = "Gen",
#        last_name = "Rich",
#        email = "ggg@gmail.com",
#        username = "GBDPMP", 
#        password = "43k9ygy5")
#        
#        self.gen_profile = Recipe (
#        Profile,
#        user = foreign_key (self.gen_user),
#        user_type = "Businessman", 
#        user_interests = "Hotels", 
#        )
#        
#        
#        self.australia_country = Recipe (
#            'IFB299app.Country',
#            name="Australia", 
#            code='Aust'
#        )
#        
#        self.queensland_region = Recipe(
#            Region,
#            name = "queensland",
#            latitude = "27.404",
#            longitude = "153.0987",
#            country_id = foreign_key(self.australia_country) 
#        )
#        self.brisbane_city = Recipe (
#        City, 
#        name = "Brisbane",
#        country_id = foreign_key(self.australia_country),
#        region_id = foreign_key(self.queensland_region),
#        latitude = "-27.1234",
#        longitude = "153.245",
#        )
#        
#        self.southbank_location = Recipe (
#        Location,
#        name = "Southbank Parklands",
#        slug = "Southbank_Parklands",
#        category_id = foreign_key (self.attraction_category),
#        city_id = foreign_key (self.brisbane_city),
#        region_id = foreign_key (self.queensland_region),
#        country_id = foreign_key (self.australia_country))
#  
#        self.music_event = Recipe (
#        Event, 
#        name = "Xavier Rudd" ,
#        description = "jskfjlsdj",
#        start_date = "1999-05-25 08:30",
#        end_date = "1999-05-25 10:30",
#        location_id = foreign_key(self.southbank_location)
#        )
#        
#        self.liked_feedback = Recipe (
#        FeedbackRecommendations,
#        placeID = "CH2356576",
#        name = "Southbank",
#        response = "True", 
#        user = foreign_key (self.gen_user),
#        )

    
    def test_index_views(self):
        url = reverse("index")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
    
    def test_register_views(self):
        url = reverse("register")
        resp = (self.client.get(url))
        self.assertEqual(resp.status_code, 200)
    
    def test_register2_views(self):
        url = reverse("register2")
        resp = (self.client.get(url))
        self.assertEqual(resp.status_code, 200)
    
    def test_login_views(self):
        url = reverse("login")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('dashboard'))
        self.assertRedirects(resp, '/IFB299app/login/?next=/IFB299app/dashboard/')
    
    
    
#    def test_logged_in_uses_correct_template(self):
#        
#        login = self.client.login(username='GBDPMP', password='43k9ygy5')
#        resp = self.client.get(reverse('dashboard'))
#        
#        #Check our user is logged in
#        self.assertEqual(str(resp.context['username']), 'GBDPMP')
#        #Check that we got a response "success"
#        self.assertEqual(resp.status_code, 200)
#
#        #Check we used correct template
#        self.assertTemplateUsed(resp, '../templates/IFB299app/dashboard')

    
        
    


