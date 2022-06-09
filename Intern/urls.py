from django.urls import path
from Intern import views as Intern_views
from student import views as Student_views
from company import views as Company_views

urlpatterns = [
    path('', Intern_views.home_page, name='home'),
    path('student-register/', Student_views.student_register, name='student-register'),
    path('student-login/', Student_views.student_login, name='student-login'),
    path('student-register/student-profile', Student_views.create_student_profile, name='student-profile'),
    path('company-register/', Company_views.company_register, name='company-register'),
    path('company-logn/', Company_views.company_login, name='company-login'),
    path('comapby-register/company-profile', Company_views.create_company_profile, name='company-profile')
]