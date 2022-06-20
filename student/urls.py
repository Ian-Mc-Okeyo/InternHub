from django.urls import path
from .views import student_dashboard, edit_student_profile, ListCompanies, view_job, apply_job, ListInternships, view_company, view_feedback, withdraw_application, view_interview_details, list_student_interviews

urlpatterns = [
    path('dashboard/', student_dashboard, name='student-dashboard'),
    path('edit-profile/', edit_student_profile, name = 'edit-student-profile'),
    path('view-companies', ListCompanies.as_view(), name='view-companies'),
    path('view-job/<int:param>', view_job, name='view-job'),
    path('view-company/<int:param>', view_company, name='view-company'),
    path('apply-job/<int:param>', apply_job, name='apply-job'),
    path('view-internships', ListInternships.as_view(), name='view-all-internships'), 
    path('view-feedback', view_feedback, name='view-feedback'),
    path('withdraw-application/<int:param>', withdraw_application, name='delete-application'),
    path('view-interview-details/<int:param>', view_interview_details, name='view-interview-details'),
    path('view-interviews', list_student_interviews, name='view-student-interviews')
]