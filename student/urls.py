from django.urls import path
from .views import student_dashboard, edit_student_profile

urlpatterns = [
    path('dashboard/', student_dashboard, name='student-dashboard'),
    path('edit-profile/', edit_student_profile, name = 'edit-student-profile'),
]