from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.company_dashboard, name='company-dashboard'),
    path('edit-profile', views.edit_company_profile, name='edit-company-profile'),
    path('post-intern-job', views.post_intern_job, name='post-intern-job'),
]