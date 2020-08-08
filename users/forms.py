from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile
from django.core.exceptions import ValidationError

class UserRegisterForm(UserCreationForm):
    email=forms.EmailField(required=True)
    first_name=forms.CharField(required=True)
    last_name=forms.CharField()


    class Meta:
        model = User
        fields=('first_name', 'last_name', 'username', 'email')


class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField()
    first_name=forms.CharField(required=True)
    last_name=forms.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['image']
