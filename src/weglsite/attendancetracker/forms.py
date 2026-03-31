from django import forms
from .models import AttendanceRecord

class AttendanceSearchForm(forms.Form):
    search = forms.CharField(label='Search by Name', max_length=200, required=False)
    sort = forms.ChoiceField(
        label='Sort by Absences',
        choices=[('asc', 'Ascending'), ('desc', 'Descending')],
        required=False,
        initial='desc'
    )
