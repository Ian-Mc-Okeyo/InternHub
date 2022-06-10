from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from pkg_resources import Requirement
from .models import Company, InternJob

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
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Kindly give a brief description of the company. What kind of skills and students you need,  what the company does, qualifications from a student... '}))

class EditCompanyProfileForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['field', 'country', 'city', 'description', 'profilePic']

class EditCompanyUserForm(forms.ModelForm):
    username = forms.CharField(label=("Company Name"))
    class Meta:
        model = User
        fields = ['username', 'email']

class DateTimePickerInput(forms.DateTimeInput):
        input_type = 'datetime'

class PostInternJobForm(forms.Form):
    choices = (
        ('', ''),
        ('Yes', 'Yes'),
        ('No', 'No')
    )
    title = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Job Title'}))
    resume = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'placeholder': 'Job Title'}), required=True, label=("Is Resume required?"))
    transcript = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'placeholder': 'Job Title'}), required=True, label=("Is Transcript required?"))
    recommendation = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'placeholder': 'Job Title'}), required=True, label=("Is Letter Of Recommendation required?"))
    cover_letter = forms.ChoiceField(choices=choices, widget=forms.Select(attrs={'placeholder': 'Job Title'}), required=True, label=("Is Cover Letter required?"))
    requirements = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Kindly list other requirements like skills, Education level and any other the company might require the intern to meet'}))
    deadline = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#datetimepicker1',
            'type': 'datetime-local'
        })
    )

    # class Meta:
    #     model= InternJob
    #     fields = ['title', 'resume', 'transcript', 'recommendation', 'cover_letter', 'deadline', 'requirements']