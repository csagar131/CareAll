from django import forms 
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User

class ElderSignupForm(UserCreationForm):

    first_name = forms.CharField()
    last_name = forms.CharField()
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','contact','password1','password2','is_elder')

    def clean(self):
        self.cleaned_data['is_elder'] = True
        return super().clean()
        
        
    
class YoungerSignupForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','contact','password1','password2')

class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('age','gender','contact','address','image')


class AddFundForm(forms.Form):
    fund = forms.IntegerField()
