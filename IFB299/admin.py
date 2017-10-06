from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import City, Region, Country, Category, Location, Event, User, Profile, Questions

class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region_id', 'country_id', 'latitude', 'longitude')

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'country_id')

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude', 'city_id')
    prepopulated_fields = {'slug':('name',)}

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_id')

# Define an inline admin descriptor for User model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = Profile
    can_delete = False

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserInline, )
    
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'object_id', 'content', 'timestamp', 'approved')


# Register your models here.

admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Questions, QuestionsAdmin)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
