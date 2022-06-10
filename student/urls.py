from django.urls import path
from .views import student_dashboard, edit_student_profile, ListCompanies

urlpatterns = [
    path('dashboard/', student_dashboard, name='student-dashboard'),
    path('edit-profile/', edit_student_profile, name = 'edit-student-profile'),
    path('view-companies', ListCompanies.as_view(), name='view-companies'),
]