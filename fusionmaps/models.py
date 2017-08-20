from django.db import models


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
