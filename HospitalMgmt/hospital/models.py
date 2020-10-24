from django.db import models
from django.utils import timezone
from django.contrib.admin.widgets import AdminDateWidget
# Create your models here.
class Doctor(models.Model):
    name=models.CharField(max_length=50)
    mobile=models.IntegerField()
    special=models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Patient(models.Model):
    name=models.CharField(max_length=50)
    gender=models.CharField(max_length=10)
    mobile=models.IntegerField()
    address=models.CharField(max_length=150)
    age = models.CharField(verbose_name='Age', max_length=3, default=0)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    confirm = models.BooleanField(verbose_name='confirm_appointment', default=False)
    name = models.CharField(verbose_name='Patient Name', max_length=30, default="")
    department = models.CharField(verbose_name='Department', max_length=30, default="")
    age = models.CharField(verbose_name='Age', max_length=3, default=0)
    date = models.DateField(verbose_name="Date", default=timezone.now())
    time = models.TimeField(verbose_name="Time", default=timezone.now())

    def __str__(self):
        return self.name


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


