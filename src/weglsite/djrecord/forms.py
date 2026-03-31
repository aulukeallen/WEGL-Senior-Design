# forms.py
from django import forms
from .models import DJ, OnAirShow

class DjInfoForm(forms.ModelForm):
    class Meta:
        model = DJ
        fields = ['firstName', 'lastName', 'email', 'joinDate']  # or '__all__'

#
class OnAirShowForm(forms.ModelForm):
    class Meta:
        model = OnAirShow
        fields = "__all__"
        widgets = {
            "startTime": forms.TimeInput(
                attrs={"type": "time", "step": "1800"}  # 30 min intervals
            )
        }