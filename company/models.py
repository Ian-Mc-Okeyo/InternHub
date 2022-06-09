from django.db import models
from django.contrib.auth.models import User

class Company(models.Model):
    user  = models.OneToOneField(User, on_delete=models.CASCADE)
    field = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    profilePic = models.ImageField(default='default.jpg', upload_to='profile_pics')