from django.contrib.auth.decorators import login_required
from  django.contrib.auth import login, logout
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.contrib.auth.views import LoginView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from render_block import render_block_to_string
import datetime

from .models import Task,User
from .forms import Login_class,User_class


class RegistrationPage(CreateView):
    template_name = "registration.html"
    form_class = User_class
    success_url = reverse_lazy("Home")
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        return context

class LoginPage(LoginView):
    template_name = "login.html"
    form_class = Login_class
    success_url = reverse_lazy("Home")


class HomePage(TemplateView):
    template_name = "home.html"

    def post(self,request,**kwargs):
        data = request.POST
        print(data)
        #user = request.user
        #text = data.get('text_of_new_task')
        #added_at = datetime.datetime.now().date()
        #deadline = data.get('deadline_of_new_task')
        #priority = data.get("tasks_priority")
        #done = False
        #task = Task(user=user, text=text, added_at=added_at,deadline=deadline, priority=priority, done=done)
        #task.save()
        #response = render_block_to_string("Post.html", "tasks", {"today": Comments.objects.filter(post=post)})
        #return HttpResponse(response)



def Logout(request):
    logout(request)
    return redirect("/")




