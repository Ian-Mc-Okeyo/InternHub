from django.db import models
from django.contrib.auth.models import User
from student.models import Student
from django.utils import timezone


class Company(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    profilePic = models.ImageField(default='default.jpg', upload_to='profile_pics')
    description = models.TextField(null=True)
    opened = models.CharField(max_length=20, null=True)

class InternJob(models.Model):
   company = models.ForeignKey(Company, on_delete=models.CASCADE)
   title = models.CharField(max_length=100, null=False)
   deadline = models.DateTimeField()
   resume = models.CharField(max_length=20)
   transcript = models.CharField(max_length=20)
   recommendation = models.CharField(max_length=20)
   cover_letter = models.CharField(max_length=20)
   requirements = models.TextField()

class JobApplication(models.Model):
    job = models.ForeignKey(InternJob, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    time_applied = models.DateTimeField(default=timezone.now)
    resume = models.FileField(upload_to='resume', null=True)
    recommendation = models.FileField(upload_to='recommendation', null=True)
    transcript = models.FileField(upload_to='transcript', null=True)
    cover_letter = models.FileField(upload_to='cover_letter', null=True)
    feedback = models.CharField(max_length=20, default = 'Pending')

class Interview(models.Model):
    job = models.ForeignKey(InternJob, on_delete = models.CASCADE)
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    time = models.DateTimeField()
    type = models.CharField(max_length=30)
    description = models.TextField()

