from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm




class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email',"password1","password2"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name',]
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number','address','image','country','city','company','headline','about','address_line_1','address_line_2','fb_link','twitter_link','instagram_link','linked_in_link']