
from django import forms

class StartServiceForm(forms.Form):
    days = forms.IntegerField()


class ReviewForm(forms.Form):
    review = forms.CharField(max_length=255)
    rating = forms.IntegerField()