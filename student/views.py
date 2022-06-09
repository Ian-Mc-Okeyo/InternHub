from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegisterForm, StudentProfileForm, StudentLoginForm, EditStudentProfileForm, EditStudentUserForm
from .models import Student
from django.contrib.auth import login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required#for login required

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
    return render(request, 'student/student_dashboard.html')

@login_required
def edit_student_profile(request):
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
