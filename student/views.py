from curses import flash
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegisterForm, StudentProfileForm, StudentLoginForm, EditStudentProfileForm, EditStudentUserForm, ApplyJobForm, RequestInternshipForm, SearchCompany
from .models import Student
from django.contrib.auth import login, logout
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required#for login required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from company.models import Company, GeneralInterview, InternJob, Interview, JobApplication, InternShipRequest

def student_missing(request):
    check_student = Student.objects.filter(user=request.user).first()
    if not check_student:
        messages.warning(request, 'Error')
        return True

def student_register(request):
    if request.method=='POST':
        form = StudentRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('student-profile')
        else:
            pass
    else:
        form = StudentRegisterForm()
    return render(request, 'student/student_register.html', {'form': form})

def student_login(request):
    if request.method=='POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password=password)
            if user is not None:
                check_student = Student.objects.filter(user=user).first()#checking if the student has created a student profile
                if check_student:
                    login(request, user)
                    messages.success(request, 'Successful login')
                    return redirect('student-dashboard')
                else:
                    messages.warning(request, 'Please create a student profile first')
                    return redirect('student-profile')
            else:
                messages.warning(request, 'Wrong User credentials')
                return redirect('student-login')
    else:
        form = StudentLoginForm()
    return render(request, 'student/student_login.html', {'form': form})

def create_student_profile(request):
    if request.method=='POST':
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.filter(username=form.cleaned_data.get('username')).first()
            if user:
                user.first_name = form.cleaned_data.get('First_name')
                user.last_name = form.cleaned_data.get('Last_name')
                user.save()
                new_student = Student(user=user, middleName = form.cleaned_data.get('Middle_name'), phoneNo=form.cleaned_data.get('phoneNumber'),
                                        school = form.cleaned_data.get('school'), course = form.cleaned_data.get('course'), yearOfStudy=form.cleaned_data.get('yearOfStudy'))
                new_student.save()
                login(request, user)
                messages.success(request, f'Profile Successfully created')
                return redirect('student-dashboard')
            else:
                messages.warning(request, 'The username does not exist')
                return redirect('student-profile')

    else:
        form = StudentProfileForm()
    
    return render(request, 'student/student_profile.html', {'form': form})

@login_required
def student_dashboard(request):
    if student_missing(request):
        logout(request)
    jobs = InternJob.objects.all()
    return render(request, 'student/student_dashboard.html', {'jobs': jobs})

@login_required
def edit_student_profile(request):
    if student_missing(request):
        logout(request)
    
    if request.method == 'POST':
        p_form = EditStudentProfileForm(request.POST, request.FILES, instance=request.user.student)
        u_form = EditStudentUserForm(request.POST, instance=request.user)
        print(request.POST)
        if 'p_form' in request.POST:
            if p_form.is_valid():
                p_form.save()
                messages.success(request, 'Profile successfully updated')
                return redirect('edit-student-profile')
            else:
                messages.warning(request, 'An Error occured')
        elif 'u_form' in request.POST: #u_form is provided as the name of the submit buttton in the html form
            if u_form.is_valid():
                u_form.save()
                messages.success(request, 'User details successfully updated')
                return redirect('edit-student-profile')
            else:
                pass
    else:
        p_form = EditStudentProfileForm(instance = request.user.student)
        u_form = EditStudentUserForm(instance=request.user)
    return render(request, 'student/edit_student_profile.html', {'p_form': p_form, 'u_form': u_form})

# class ListCompanies(LoginRequiredMixin, ListView):
#     model = Company
#     template_name= 'student/view_companies.html'
#     context_object_name = 'Companies'
#     paginate_by = 5

#     def get_context_data(self, **kwargs):
#         context = super(ListCompanies, self).get_context_data(**kwargs)
#         context['form'] = SearchCompany()
#         return context

@login_required
def ListCompanies(request):
    Companies = Company.objects.all()
    if request.method == 'POST':
        form = SearchCompany(request.POST)
        if form.is_valid():
            company_name = form.cleaned_data.get('name')
            user = User.objects.filter(username=company_name).first()
            if user:
                company = Company.objects.filter(user=user).first()
                if company:
                    return redirect('view-company', param=company.pk)
            else:
                messages.warning(request, 'Company does not exist')
                return redirect('view-companies')
    else:
        form = SearchCompany()
    context = {
        'Companies': Companies,
        'form': form

    }
    return render(request, 'student/view_companies.html', context=context)

class ListInternships(LoginRequiredMixin, ListView):
    model = InternJob
    template_name = 'student/view_internships.html'
    context_object_name = 'Internships'
    paginate_by = 5

@login_required
def view_job(request, param):
    if student_missing(request):
        logout(request)
    
    job = InternJob.objects.filter(pk=param).first()
    if not job:
        messages.warning(request, 'Job does not exist')
        return redirect('student-dashboard')
    
    doc_req = ''
    if job.transcript == 'No' and job.recommendation == 'No' and job.resume == 'No' and job.cover_letter == 'No':
        doc_req='No Document Required'
    return render(request, 'student/view_job.html', {'job': job, 'doc_req': doc_req})

@login_required
def view_company(request, param):
    if student_missing(request):
        logout(request)
    
    company = Company.objects.filter(pk=param).first()
    print(company.internjob_set.all()) #querying all the internjobs of the company
    if not company:
        messages.warning(request, 'Wrong Comany Page')
        return redirect('student-dashboard')
    
    return render(request, 'student/view_company.html', {'company': company})

@login_required
def apply_job(request, param):
    if student_missing(request):
        logout(request)
    
    job = InternJob.objects.filter(pk=param).first()
    student = Student.objects.filter(user = request.user).first()
    check_application = JobApplication.objects.filter(job=job, student=student).first()
    if check_application:
        messages.warning(request, 'You already applied for this intern job')
        return redirect('view-job', param=param)
    else:
        if request.method == 'POST':
            form = ApplyJobForm(request.POST, request.FILES)
            if form.is_valid:
                current_student = Student.objects.filter(user=request.user).first()
                new_application = JobApplication(student= current_student, job=job)
                if job.resume=='Yes':
                    new_application.resume = request.FILES['resume']
                if job.recommendation == 'Yes':
                    new_application.recommendation = request.FILES['recommendation']
                if job.transcript == 'Yes':
                    new_application.transcript = request.FILES['transcript']
                if job.cover_letter == 'Yes':
                    new_application.cover_letter = request.FILES['cover_letter']
                
                new_application.save()
                messages.success(request, 'Application has been Sent')
                return redirect('view-job', param=param)
        else:
            form = ApplyJobForm()
    doc_req = ''
    if job.transcript == 'No' and job.recommendation == 'No' and job.resume == 'No' and job.cover_letter == 'No':
        doc_req='Are You sure you want to make This application?'
    
    context = {
        'form': form, 
        'job': job, 
        'doc_req': doc_req
    }
    return render(request, 'student/apply_job.html', context=context)

@login_required
def view_feedback(request):
    student = Student.objects.filter(user=request.user).first()
    applications = JobApplication.objects.filter(student=student).all()

    context = {
        'applications': applications
    }
    return render(request, 'student/view_feedback.html', context=context)

@login_required
def withdraw_application(request, param):
    if student_missing(request):
        logout(request)
    
    application = JobApplication.objects.filter(pk=param).first()
    application.delete()
    messages.success(request, 'Application Successfully Deleted 🫤')
    return redirect('view-feedback')

@login_required
def view_interview_details(request, param):
    if student_missing(request):
        logout(request)
    
    application = JobApplication.objects.filter(pk=param).first()
    interview = Interview.objects.filter(job=application.job, student=application.student).first()
    print(interview.job.title)
    return render(request, 'student/view_interview_details.html', {'interview': interview})

@login_required
def list_student_interviews(request):
    if student_missing(request):
        logout(request)
    
    student = Student.objects.filter(user=request.user).first()
    interviews = Interview.objects.filter(student=student).all()
    general_interviews = GeneralInterview.objects.filter(student=student).all()
    return render(request, 'student/view_student_views.html', {'interviews': interviews, 'general': general_interviews})

@login_required
def request_internship(request, compk):
    if student_missing(request):
       logout(request)
    
    student = Student.objects.filter(user = request.user).first()
    company = Company.objects.filter(pk=compk).first()
    check_application = InternShipRequest.objects.filter(student=student, company=company).first()
    if check_application:
        messages.warning(request, 'You already applied for this job')
        return redirect('view-companies')
    
    if request.method == 'POST':
        form = RequestInternshipForm(request.POST, request.FILES)
        if form.is_valid:
            new_request = InternShipRequest(student=student, company=company, resume=request.FILES['resume'])
            new_request.save()
            messages.success(request, 'Request successfully made')
            return redirect('view-companies')
        else:
            for error in form.errors:
                messages.warning(request, form.errors[error])
    else:
        form = RequestInternshipForm()
    return render(request, 'student/request_internship.html', {'form': form})
