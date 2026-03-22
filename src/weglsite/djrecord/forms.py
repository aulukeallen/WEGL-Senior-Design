# forms.py
from django import forms
from .models import DJ

class DjInfoForm(forms.ModelForm):
    class Meta:
        model = DJ
        fields = ['firstName', 'lastName', 'email', 'joinDate']  # or '__all__'