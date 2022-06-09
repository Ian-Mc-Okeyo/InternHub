from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Student

class StudentRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model=User
        fields=['username', 'email', 'password1', 'password2']

class StudentLoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Please provide your registered username'}))
    password = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))

class StudentProfileForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off", 'placeholder': 'Please provide your registered username'}))
    First_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    Middle_name = forms.CharField(required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    Last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    phoneNumber = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}), max_length=14, min_length=10)
    school = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    course = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    yearOfStudy = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))

class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phoneNo', 'course', 'yearOfStudy', 'school', 'profilePic']

class EditStudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']