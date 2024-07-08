from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    pass

class Task (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=750)
    added_at = models.CharField(max_length=50)
    deadline = models.CharField(max_length=50)
    priority = models.CharField(max_length=20)
    done = models.BooleanField()
