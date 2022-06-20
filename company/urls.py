from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company-dashboard'),
    path('edit-profile/', views.edit_company_profile, name='edit-company-profile'),
    path('post-intern-job/', views.post_intern_job, name='post-intern-job'),
    path('view-interns', views.ListAvailableIternsView.as_view(), name='company-view-interns'),
    path('view-job-applications', views.view_company_job_applications, name='job-applications'),
    path('view-job-applicants/<int:param>', views.view_job_applicants, name='job-applicants'),
    path('reject-job-applicant/<int:jobpk>/<int:applpk>', views.reject_job_application, name='reject-application'),
    path('create-interview/<int:param>', views.createInterview, name='create-interview')
]