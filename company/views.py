from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages

from student.models import Student
from .forms import CompanyRegisterForm, CompanyProfileForm, CompanyLoginForm, EditCompanyProfileForm, EditCompanyUserForm, PostInternJobForm, CreateInterviewForm
from .models import Company, InternJob, Interview, JobApplication
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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
                check_student = Student.objects.filter(user=user).first()
                check_company = Company.objects.filter(user=user).first()#checking if the company has created a company profile
                if check_student:
                    messages.warning(request, 'Mbwakni, you are a Student 😡😡!!')
                    return redirect('student-login')
                elif check_company:
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
                    city = form.cleaned_data.get('city'), description = form.cleaned_data.get('description'))
                new_company.save()
                login(request, user)
                messages.success(request, 'Profile successfully created')
                return redirect('company-dashboard')
        else:
            pass
    else:
        form = CompanyProfileForm()
    return render(request, 'company/company_profile.html', {'form': form})

@login_required
def company_dashboard(request):
    interns = Student.objects.all()
    return render(request, 'company/company_dashboard.html', {'interns': interns})

@login_required
def edit_company_profile(request):
    if request.method == 'POST':
        p_form = EditCompanyProfileForm(request.POST, request.FILES, instance=request.user.company)
        u_form = EditCompanyUserForm(request.POST, instance=request.user)
        print(request.POST)
        if 'p_form' in request.POST:
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profile successfully updated')
                return redirect('edit-company-profile')
            else:
                messages.warning(request, 'An Error occured')
        elif 'u_form' in request.POST: #u_form is provided as the name of the submit buttton in the html form
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'Company details successfully updated')
                return redirect('edit-company-profile')
            else:
                pass
    else:
        p_form = EditCompanyProfileForm(instance = request.user.company)
        u_form = EditCompanyUserForm(instance=request.user)
    return render(request, 'company/edit_company_profile.html', {'p_form': p_form, 'u_form': u_form})

@login_required
def post_intern_job(request):
    if request.method=='POST':
        form = PostInternJobForm(request.POST)
        if form.is_valid():
            company = Company.objects.filter(user = request.user).first()
            new_job = InternJob(company=company, title=form.cleaned_data.get('title'), deadline=form.cleaned_data.get('deadline'), resume=form.cleaned_data.get('resume'), 
                    recommendation = form.cleaned_data.get('recommendation'), transcript=form.cleaned_data.get('transcript'), cover_letter=form.cleaned_data.get('cover_letter'), 
                    requirements=form.cleaned_data.get('requirements'))
            new_job.save()
            messages.success(request, 'Job has been successfully posted')
            return redirect('post-intern-job')
    else:
        form = PostInternJobForm()
    return render(request, 'company/post_intern_job.html', {'form': form})

class ListAvailableIternsView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'company/view_available_interns.html'
    context_object_name = 'Interns'
    paginate_by = 5

@login_required
def view_company_job_applications(request):
    company = Company.objects.filter(user=request.user).first()
    jobs = InternJob.objects.filter(company=company).all()
    context = {
        'jobs': jobs
    }
    return render(request, 'company/view_comp_job_appl.html', context=context)

@login_required
def view_job_applicants(request, param):
    job = InternJob.objects.filter(pk=param).first()
    applications = job.jobapplication_set.filter(feedback='Pending').all()
    context = {
        'applications': applications, 
        'job': job
    }
    print(job.recommendation)
    return render(request, 'company/view_job_applicants.html', context=context)

@login_required
def reject_job_application(request, jobpk, applpk):
    application = JobApplication.objects.filter(pk=applpk).first()
    application.feedback='Rejected'
    application.save()
    messages.success(request, 'Application has been successfullly rejected')
    return redirect('job-applicants', param=jobpk)

@login_required
def createInterview(request, param):
    application = JobApplication.objects.filter(pk=param).first()
    if request.method == 'POST':
        form = CreateInterviewForm(request.POST)
        if form.is_valid():
            interview = Interview(job=application.job, student=application.student, time=form.cleaned_data.get('time'), type=form.cleaned_data.get('type'), 
                                        description=form.cleaned_data.get('description'))
            application.feedback = 'Accepted'
            application.save()
            interview.save()
            messages.success(request, 'Interview has been successfully Scheduled')
            return redirect('job-applicants', param=application.job.pk)
    else:
        form = CreateInterviewForm()
    
    context = {
        'form': form,
        'application': application
    }
    return render(request, 'company/create_interview.html', context=context)
