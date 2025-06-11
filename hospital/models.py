from django.db import models

class HospitalSupplyData(models.Model):
    item_code = models.CharField(max_length=100)
    item_description = models.CharField(max_length=200)
    patient_footfall = models.IntegerField()
    last_week_usage = models.IntegerField()
    public_holiday = models.BooleanField()
    rain_impact = models.BooleanField()
    quantity_used = models.IntegerField()
    week_number = models.IntegerField()

    def __str__(self):
        return f"{self.item_code} - Week {self.week_number}"