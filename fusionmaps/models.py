from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User

# from oauth2client.contrib.django_util.models import CredentialsField


class GeoLocation(models.Model):
    lat = models.CharField(max_length=30)
    lng = models.CharField(max_length=30)
    address = models.CharField(max_length=120)

    def __str__(self):
        return self.address

    def __eq__(self, other):
        if (self.lat == other.lat and self.lng == other.lng):
            return True
        return False

    @classmethod
    def create(cls, lat, lng, address):
        location = cls(lat=lat, lng=lng, address=address)
        # do something with the book
        return location


# class CredentialsModel(models.Model):
#     id = models.ForeignKey(User, primary_key=True)
#     credential = CredentialsField()
#
#
# class CredentialsAdmin(admin.ModelAdmin):
#     pass
