from django import forms

class CSVUploadForm(forms.Form):
    csvFile = forms.FileField(label='Select an Asplay Report CSV', 
               help_text="Columns expected: CUT, TITLE, ARTIST, ALBUM, GROUP, DATE, ACTSTART, ACTDUR")
    