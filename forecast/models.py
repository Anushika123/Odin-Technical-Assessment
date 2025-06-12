from django.db import models

# Create your models here.

# forecast/models.py

from django.db import models

class ForecastData(models.Model):
    item_code = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255)
    week = models.DateField()
    patient_footfall = models.IntegerField()
    last_week_usage = models.IntegerField()
    public_holiday = models.BooleanField()
    rain_impact = models.BooleanField()
    quantity_used = models.IntegerField()

    def __str__(self):
        return f"{self.item_code} ({self.week})"
