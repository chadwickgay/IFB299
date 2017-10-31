from django.test import TestCase
from IFB299app.models import (Location, User, Profile, Category, FeedbackRecommendations, Country, Region, City, Event)
from model_mommy import mommy
from model_mommy.recipe import (Recipe, foreign_key)
from django.utils import timezone
from django.core.urlresolvers import reverse
from IFB299app.forms import LoginForm, RegisterForm, ProfileForm

class ModelFinderTest(TestCase):
    
#    def create_account (self, first_name="Gen", last_name="Richards", email="ggg@gmail.com", username="GBDPD" ):
#        return User.objects.create(first_name=first_name, last_name=last_name, email=email, username=username)
    

    
    def create_category (self, name="Shopping"):
        return Category.objects.create(name=name)
    
    def test_create_category(self):
        w = self.create_category()
        self.assertTrue(isinstance(w, Category))
        self.assertEqual(w.__str__(), w.name)
    
    def create_country (self, name="Australia", code='Aust'):
        return Country.objects.create(name=name, code=code)
    
    def test_create_country(self):
        w = self.create_country()
        self.assertTrue(isinstance(w, Country))
        self.assertEqual(w.__str__(), '%s (%s)' % (w.name, w.code))
    
    def setUp (self):
        """Setting up all the tests"""

        self.attraction_category = Recipe (
        Category,
        name="attraction",
        )
        
        self.gen_user = Recipe (
        User, 
        first_name = "Gen",
        last_name = "Rich",
        email = "ggg@gmail.com",
        username = "GBDPMP")
        
        self.australia_country = Recipe (
            'IFB299app.Country',
            name="Australia", 
            code='Aust'
        )
        
        self.queensland_region = Recipe(
            Region,
            name = "queensland",
            latitude = "27.404",
            longitude = "153.0987",
            country_id = foreign_key(self.australia_country) 
        )
        self.brisbane_city = Recipe (
        City, 
        name = "Brisbane",
        country_id = foreign_key(self.australia_country),
        region_id = foreign_key(self.queensland_region),
        latitude = "-27.1234",
        longitude = "153.245",
        )
        
        self.southbank_location = Recipe (
        Location,
        name = "Southbank Parklands",
        slug = "Southbank_Parklands",
        category_id = foreign_key (self.attraction_category),
        city_id = foreign_key (self.brisbane_city),
        region_id = foreign_key (self.queensland_region),
        country_id = foreign_key (self.australia_country))
  
        self.music_event = Recipe (
        Event, 
        name = "Xavier Rudd" ,
        description = "jskfjlsdj",
        start_date = "1999-05-25 08:30",
        end_date = "1999-05-25 10:30",
        location_id = foreign_key(self.southbank_location)
        )
        
        self.liked_feedback = Recipe (
        FeedbackRecommendations,
        placeID = "CH2356576",
        name = "Southbank",
        response = "True", 
        user = foreign_key (self.gen_user),
        )
    def test_create_account(self):
        w = self.gen_user.make()
        self.assertTrue(isinstance(w, User))
        self.assertEqual(w.__str__(), w.username)
    def test_check_Region(self):
        w = self.queensland_region.make()
        self.assertTrue(isinstance(w, Region))
        self.assertEqual(w.__str__(), w.name)
    
    def test_check_city(self):
        w = self.brisbane_city.make()
        self.assertTrue(isinstance(w, City))
        self.assertEqual(w.__str__(), w.name)
        
    def test_check_location (self):
        w = self.southbank_location.make()
        self.assertTrue(isinstance(w, Location))
        self.assertEqual(w.__str__(), w.name)
    
    def test_check_event (self):
        w = self.music_event.make()
        self.assertTrue(isinstance(w, Event))
        self.assertEqual(w.__str__(), w.name)
        
    def test_check_feedback(self):
        w = self.liked_feedback.make()
        self.assertTrue(isinstance(w, FeedbackRecommendations))
        self.assertTrue(w.__str__(), w.placeID)
    
    