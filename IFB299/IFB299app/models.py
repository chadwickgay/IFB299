from django.db import models
from datetime import datetime

# Create your models here.

class Category(models.Model):
    """
    Model representing a location category (e.g. Colleges, Parks, Mueseums etc.).
    """
    name = models.CharField(max_length=200, help_text="Enter a location category (e.g. Colleges, Parks, Mueseums etc.)")
    
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        """
        String for representing the Model object (in Admin site etc.)
        """
        return self.name

class Country(models.Model):
    """
    Model representing a country.
    """
    name = models.CharField(max_length=255, help_text="Enter a country (e.g. Australia, New Zealand, China etc.)")
    code = models.CharField(max_length=10, help_text="Enter a country code (e.g. AUS, NZ, CHN etc.)")

    class Meta:
        verbose_name_plural = 'Countries'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.name, self.code)

class Region(models.Model):
    """
    Model representing a region (regions/provinces/states).
    """
    name = models.CharField(max_length=255, help_text="Enter a region (region/province/state)")
    code = models.CharField(max_length=10, help_text="Enter a region code (e.g. QLD, NSW, VIC etc.)")
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s (%s)' % (self.name, self.code)

class City(models.Model):
    """
    Model representing a city.
    """
    name = models.CharField(max_length=255, help_text="Enter a city (e.g. Brisbane, Sydney, Perth etc.)")
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Cities'

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name

class Location(models.Model):
    """
    Model representing a location
    """
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, help_text="Enter the street address (e.g. 123 Evergreen Tce)")
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the location")
    ## Lat/Long
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    ## FK
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name   

class Event(models.Model):
    """
    Model representing a event
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, help_text="Enter a brief description of the event")
    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now, blank=True)
    ##FK
    location_id = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.name   


