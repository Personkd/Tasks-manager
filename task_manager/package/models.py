from django.db import models
from django.contrib.auth.models import AbstractUser

class User (AbstractUser):
    pass

class Task (models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.CharField(max_length=750)
    added_at = models.DateField(max_length=50)
    deadline = models.DateField(max_length=50)
    priority = models.CharField(max_length=50)
    done = models.BooleanField()

    @staticmethod
    def sort (sorting_tag,request):
        if sorting_tag == 'incompleted':
            tasks = Task.objects.filter(user=request.user,done=False)
        elif sorting_tag == 'completed':
            tasks = Task.objects.filter(user=request.user,done=True)
        elif sorting_tag == 'creation_date':
            tasks = Task.objects.filter(user=request.user).order_by("added_at")
        elif sorting_tag == 'deadline':
            tasks = Task.objects.filter(user=request.user).order_by("deadline")
        elif sorting_tag == 'priority':
            tasks = Task.objects.filter(user=request.user).order_by("priority")
        elif sorting_tag == None:
            tasks = None
        if len(tasks) == 0:
            tasks = None
        return(tasks)
