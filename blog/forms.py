from django import forms
from .models import *

class NameForm(forms.ModelForm):
    name=forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-4',
            'id': 'defaultSubscriptionFormName',
            'placeholder': "Name",
            'required': 'required'
        }
    ))

    email=forms.CharField(max_length=100, widget=forms.EmailInput(
        attrs={
            'class': 'form-control mb-4',
            'id': 'defaultSubscriptionFormEmail',
            'placeholder': "Email",
            'required': 'required'
        }
    ))

    class  Meta:
        model=NameModel
        fields=('name','email')
