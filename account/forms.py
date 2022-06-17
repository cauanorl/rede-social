from django import forms
from django.contrib.auth.models import User

from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'first_name']
    
    password = forms.CharField(
        max_length=30, widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(
        max_length=30, widget=forms.PasswordInput, label="Repeat password")
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
            
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['date_of_birth', 'photo']

