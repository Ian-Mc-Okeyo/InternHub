from django.urls import path
from .views import student_dashboard, edit_student_profile, ListCompanies, view_job, apply_job, ListInternships, view_company

urlpatterns = [
    path('dashboard/', student_dashboard, name='student-dashboard'),
    path('edit-profile/', edit_student_profile, name = 'edit-student-profile'),
    path('view-companies', ListCompanies.as_view(), name='view-companies'),
    path('view-job/<int:param>', view_job, name='view-job'),
    path('view-company/<int:param>', view_company, name='view-company'),
    path('apply-job/<int:param>', apply_job, name='apply-job'),
    path('view-internships', ListInternships.as_view(), name='view-all-internships')
]