from django.contrib.auth.decorators import login_required
from  django.contrib.auth import login, logout
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView,UpdateView,FormView
from django.views.generic.base import TemplateView
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView

from render_block import render_block_to_string
import datetime

from .models import Task,User
from .forms import Login_class,User_class,Create_task_class

from .mixins import IsAuthenticated


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


class HomePage(IsAuthenticated,TemplateView):
    template_name = "home.html"

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        context["today"] = Task.objects.filter(user=user, deadline=datetime.date.today())
        context["tomorrow"] = Task.objects.filter(user=user, deadline=datetime.date.today() + datetime.timedelta(days=1))
        context["the_day_after_tomorrow"] = Task.objects.filter(user=user, deadline=datetime.date.today() + datetime.timedelta(days=2))
        return context

class TaskListPage(IsAuthenticated,TemplateView):
    template_name = "tasklist.html"

    def post(self,request,**kwargs):
        tasks=Task.sort(request.POST.get('sorting_tag'),request)
        response = render_block_to_string("tasklist.html", "tasks", {"tasklist": tasks})
        return HttpResponse(response)

class CreateTaskPage (IsAuthenticated,CreateView): #фіксити
    form_class = Create_task_class
    template_name = "home.html"
    success_url = "/home/"

    #def post(self, request, **kwargs):
        #data = request.POST
        #print(data)
        #user = request.user
        #text = data.get('text_of_new_task')
        #added_at = datetime.datetime.now().date()
        #deadline = data.get('deadline_of_new_task')
        #priority = data.get("task_priority")
        #done = False
        #task = Task(user=user, text=text, added_at=added_at, deadline=deadline, priority=priority, done=done)
        #task.save()
        #tasks_today = Task.objects.filter(user=user, deadline=datetime.date.today())
        #tasks_tomorrow = Task.objects.filter(user=user, deadline=datetime.date.today() + datetime.timedelta(days=1))
        #tasks_the_day_after_tomorrow = Task.objects.filter(user=user,deadline=datetime.date.today() + datetime.timedelta(days=2))
        #response = render_block_to_string("home.html", "tasks", {
            #"today": tasks_today,
            #"tomorrow": tasks_tomorrow,
            #"the_day_after_tomorrow": tasks_the_day_after_tomorrow
        #})
        #return HttpResponse(response)

    def get_success_url(self):
        print("123")
        user = self.request.user
        tasks_today = Task.objects.filter(user=user,deadline=datetime.date.today())
        tasks_tomorrow = Task.objects.filter(user=user,deadline=datetime.date.today() + datetime.timedelta(days=1))
        tasks_the_day_after_tomorrow = Task.objects.filter(user=user,deadline=datetime.date.today() + datetime.timedelta(days=2))
        response = render_block_to_string("home.html", "tasks", {
            "today":tasks_today,
            "tomorrow":tasks_tomorrow,
            "the_day_after_tomorrow":tasks_the_day_after_tomorrow
        })
        return HttpResponse(response)


class EditTaskPage(IsAuthenticated,TemplateView): #зробити через апдейт
    template_name = "task.html"
    def post(self,request,**kwargs):
        data = request.POST
        print(data)
        task = Task.objects.get(id=kwargs["pk"])
        if data.get("new_task_text") is not None:
            task.text=data.get("new_task_text")
        if data.get("new_task_deadline") is not None:
            task.deadline=data.get("new_task_deadline")
        if data.get("new_task_priority") is not None:
            task.priority=data.get("new_task_priority")
        if data.get("new_task_state") is not None:
            if data.get("new_task_state") == "done":
                task.done = True
            else:
                task.done = False
        task.save()
        response = render_block_to_string("task.html", "task", {
            "old_text": task.text,
            "old_deadline": task.deadline,
            "old_priority": task.priority,
            "old_state": task.done
        })
        return HttpResponse(response)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.get(id=kwargs["pk"])
        context["task"] = task
        context["old_text"] = task.text
        context["old_deadline"] = task.deadline
        context["old_priority"] = task.priority
        context["old_state"] = task.done
        return context


class ProfileEditPage(IsAuthenticated,TemplateView): #зробити через апдейтвью
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["username"] = user
        context["email"] = user.email
        return context

    def post(self,request,**kwargs):
        data = request.POST
        print(data)
        user = request.user
        new_username = data.get("new_username")
        new_email = data.get("new_email")
        user.username = new_username
        user.email = new_email
        user.save()
        response = render_block_to_string("profile.html", "user", {
            "username": user.username,
            "email": user.email
        })
        return HttpResponse(response)

class DeleteTaskPage(IsAuthenticated,TemplateView):
    template_name = "tasklist.html"
    def post(self,request,**kwargs):
        task = Task.objects.get(id=kwargs["pk"])
        task.delete()
        tasks = Task.sort(request.POST.get('sorting_tag'), request)
        response = render_block_to_string("tasklist.html", "tasks", {"tasklist": tasks})
        return HttpResponse(response)

def Logout(request):
    logout(request)
    return redirect("/")


class Test(IsAuthenticated,CreateView):
    form_class = Create_task_class
    template_name = "test.html"


