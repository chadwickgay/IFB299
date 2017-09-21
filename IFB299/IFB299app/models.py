from django.db import models

# Create your models here.
class User(models.Model):
firstname = models.Charfield(max_length = 100)
lastname = models.Charfield(max_length = 100)
email = models.Charfield(max_length = 250)
password = models.Charfield(max_length = 100)
signupdate = models.DateTimeField(auto_now_add = True)
favourites = #foreignkey to Favourites
administrator = models.Charfield(max_length = 5)


class Location (models.Model):
name = models.Charfield(max_length = 250)
reviews = models.Charfield(max_length = 1000)
description = models.Charfield(max_length = 500)

class Favourites (models.Model):
name = models.ForeignKey(Location, on_delete = models.CASCADE)
#add other columns

