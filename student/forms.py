from dataclasses import fields
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from numpy import require

from company.models import JobApplication
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
    field = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off", 'placeholder': 'Your field of Interest'}))
    headline = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off", 'placeholder': 'Your Profile Headline'}), max_length=30)

class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['phoneNo', 'course', 'yearOfStudy', 'school', 'field', 'headline', 'profilePic']

class EditStudentUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ApplyJobForm(forms.ModelForm):
    resume = forms.FileField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'customefile'}))
    recommendation = forms.FileField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'customefile'}))
    transcript = forms.FileField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'customefile'}))
    cover_letter = forms.FileField(required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'type': 'file', 'id': 'customefile'}))
    class Meta:
        model= JobApplication
        fields = ['resume', 'recommendation', 'transcript', 'cover_letter']