from django.contrib import admin
from .models import City, Region, Country, Category, Location, Event

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

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'location_id')

# Register your models here.

admin.site.register(City, CityAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Event, EventAdmin)
