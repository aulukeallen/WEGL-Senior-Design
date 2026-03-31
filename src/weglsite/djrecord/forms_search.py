from django import forms

class DJSearchForm(forms.Form):
    search = forms.CharField(label='Search', max_length=100, required=False)
