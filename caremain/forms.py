
from django import forms

class StartServiceForm(forms.Form):
    days = forms.IntegerField()