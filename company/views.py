from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CompanyRegisterForm, CompanyProfileForm, CompanyLoginForm
from .models import Company
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def company_register(request):
    if request.method=='POST':
        form = CompanyRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('company-profile')
        else:
            pass
    else:
        form = CompanyRegisterForm()
    return render(request, 'company/company_register.html', {'form': form})

def company_login(request):
    if request.method=='POST':
        form = CompanyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('company_name')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
                check_company = Company.objects.filter(user=user).first()#checking if the company has created a company profile
                if check_company:
                    login(request, user)
                    messages.success(request, 'Successful login')
                    return redirect('company-dashboard')
                else:
                    messages.warning(request, 'Please create a company profile first')
                    return redirect('company-profile')
            else:
                messages.warning(request, 'Wrong Company credentials')
                return redirect('company-login')
    else:
        form = CompanyLoginForm()
    return render(request, 'company/company_login.html', {'form': form})

def create_company_profile(request):
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data.get('company_name')).first()
            if user:
                new_company = Company(user = user, field=form.cleaned_data.get('field'), country = form.cleaned_data.get('country'), 
                    city = form.cleaned_data.get('city'))
                new_company.save()
                login(request, user)
                messages.success(request, 'Profile successfully created')
                return redirect('company-dashboard')
        else:
            pass
    else:
        form = CompanyProfileForm()
    return render(request, 'company/company_profile.html', {'form': form})

def company_dashboard(request):
    return render(request, 'company/company_dashboard.html')

