from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

# User Sign up form shown in the register page
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
# This form is extended with standard user form
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('occupation', )

# Update user details form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('occupation', 'bio', 'profile_image' )
        exclude = ['user']
        
        
