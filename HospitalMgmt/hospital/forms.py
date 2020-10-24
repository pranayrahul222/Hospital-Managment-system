from .models import *
from django import forms
from django.contrib.admin.widgets import *


class AppointmentForm(forms.ModelForm):
    date = forms.DateField(label="Date", widget=forms.SelectDateWidget(years=range(2020, 2021)))
    time = forms.CharField(label="Time")

    class Meta:
        model = Appointment
        fields = ('name', 'department', 'date', 'time')

