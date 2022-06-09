from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CompanyRegisterForm(UserCreationForm):
    email = forms.EmailField()
    username = forms.CharField(label=("Company Name"))

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

class CompanyLoginForm(forms.Form):
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please provide your registered username'}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))

class CompanyProfileForm(forms.Form):
    company_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please provide your registered company name'}))
    country = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    field = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))