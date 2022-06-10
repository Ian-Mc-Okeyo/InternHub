from django.db import models
from django.contrib.auth.models import User


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