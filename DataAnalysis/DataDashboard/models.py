from django.db import models

class Data(models.Model):
    Hospital = models.CharField(max_length = 100)
    Beds_Cap = models.IntegerField()
    Beds_occ = models.IntegerField()
    Max_Vent = models.IntegerField()
    Active_vent = models.IntegerField()
    Active_Covid = models.IntegerField()
    Max_ICU = models.IntegerField()
    Active_ICU = models.IntegerField()

    def __str__(self):
        return self.Hospital

