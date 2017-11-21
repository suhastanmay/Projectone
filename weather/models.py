from django.db import models
from datetime import time
import datetime
import time

#creating table for sensor readings
class plant(models.Model):
    pid1 = models.IntegerField(primary_key=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    def __str__(self):
        return str(self.pid1)

#different fields are created for the class sensorreadings
class sensorreadings(models.Model):
    pid = models.ForeignKey(plant,null=True,on_delete=models.CASCADE)
    temp = models.CharField(max_length=30)
    humd = models.CharField(max_length=50)
    moi = models.CharField(max_length=50)
    date = models.CharField(max_length=150)
    detect = models.CharField(max_length=20)
    level = models.CharField(max_length=30)
    rain = models.CharField(max_length=30)

    def __str__(self):
        return self.temp