from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from multiselectfield import MultiSelectField
from django.template.defaultfilters import slugify

# Create your models here.

USER_TYPES = (
    ('Tourist', 'Tourist'),
    ('Student', 'Student'),
    ('Businessman', 'Businessman'),
)

USER_INTERESTS = (
    ('Colleges', 'Colleges'),
    ('Libraries', 'Libraries'),
    ('Industries', 'Industries'),
    ('Hotels', 'Hotels'),
    ('Parks', 'Parks'),
    ('Zoos', 'Zoos'),
    ('Museums', 'Museums'),
    ('Restaurants', 'Restaurants'),
    ('Malls', 'Malls'),
)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=500, blank=True)
    # add in photo
    user_type = models.CharField(max_length=50, choices=USER_TYPES)
    user_interests = MultiSelectField(choices=USER_INTERESTS, max_length=500)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



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
    ## Lat/Long
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    ## Slug
    slug = models.SlugField()
    ## FK
    city_id = models.ForeignKey(City, on_delete=models.CASCADE)
    region_id = models.ForeignKey(Region, on_delete=models.CASCADE)
    country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name) 
        super(Location, self).save(*args, **kwargs)
    
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