from lib2to3.pgen2 import driver
from django.db import models

# Create your models here.
class Appointment(models.Model):
    driver = models.IntegerField()
    date = models.DateField()
    hora = models.TimeField()
    lat_origin = models.IntegerField()
    lng_origin = models.IntegerField()
    lat_destination = models.IntegerField()
    lng_destination = models.IntegerField()
    description = models.CharField(max_length=100, blank=True, null=True)