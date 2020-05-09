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

class ContactForm(forms.ModelForm):
    name=forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-4',
            'id': 'defaultContactFormName',
            'placeholder': "Name",
            'required': 'required'
        }
    ))

    email=forms.CharField(max_length=100, widget=forms.EmailInput(
        attrs={
            'class': 'form-control mb-4',
            'id': 'defaultContactFormEmail',
            'placeholder': "Email",
            'required': 'required'
        }
    ))

    message=forms.CharField(max_length=500, widget=forms.Textarea(
        attrs={
            'class': 'form-control mb-4',
            'id': 'defaultContactFormMessage',
            'placeholder': "Message",
            'row': '5'
        }
    ))

    class  Meta:
        model=ContactModel
        fields=('name','email','message')
