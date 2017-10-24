from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import City, Region, Country, Category, Location, Event, User, Profile, FeedbackRecommendations

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_id', 'country_id', 'latitude', 'longitude')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country_id')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city_id')
    prepopulated_fields = {'slug':('name',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_id')

class FeedbackRecommendationsAdmin(admin.ModelAdmin):
    list_display = ('user', 'placeID', 'name')

# Define an inline admin descriptor for User model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )

# Register your models here.

admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(FeedbackRecommendations, FeedbackRecommendationsAdmin)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
