from django.contrib.auth.models import User
from django import forms

#forms are created to add new users , add plants and also to remove plants

#the following class adds new user form and also creates approp0riate fields
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
     model = User
     fields = ['username','email','password']

#the following class add new plants
class plantForm(forms.Form):
    pid1 = forms.CharField(max_length=100)
    latitude = forms.CharField(max_length=100)
    longitude = forms.CharField(max_length=100)

#the following class deletes the plant
class deleteForm(forms.Form):
    pid1 = forms.CharField(max_length=100)

