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

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context["tasks_today"] = Task.objects.filter(deadline=datetime.date.today())
        context["tasks_tomorrow"] = Task.objects.filter(deadline=datetime.date.today() + datetime.timedelta(days=1))
        context["tasks_the_day_after_tomorrow"] = Task.objects.filter(deadline=datetime.date.today() + datetime.timedelta(days=2))
        return context

class TaskListPage(TemplateView):
    template_name = "tasklist.html"

    def post(self,request,**kwargs):
        data = request.POST
        tag = data.get("sorting_tag")
        if tag is "incompleted":
            tasks = Task.objects.filter(user=request.user,done=False)
        elif tag is "completed":
            tasks = Task.objects.filter(user=request.user,done=True)
        elif tag is "creation_date":
            tasks = Task.objects.filter(user=request.user).order_by("task__creation_date")
        elif tag is "deadline":
            tasks = Task.objects.filter(user=request.user).order_by("task__deadline")
        elif tag is "priority":
            tasks = Task.objects.filter(user=request.user).order_by("task__priority")
        elif tag is None:
            tasks = None
        response = render_block_to_string("tasklist.html", "posts", {"tasks": tasks})
        return HttpResponse(response)

class CreateTaskPage (TemplateView):
    template_name = "home.html"

    def post(self,request,**kwargs):
        data = request.POST
        print(data)
        user = request.user
        text = data.get('text_of_new_task')
        added_at = datetime.datetime.now().date()
        deadline = data.get('deadline_of_new_task')
        priority = data.get("task_priority")
        done = False
        task = Task(user=user, text=text, added_at=added_at,deadline=deadline, priority=priority, done=done)
        task.save()
        tasks_today = Task.objects.filter(user=user,deadline=datetime.date.today())
        tasks_tomorrow = Task.objects.filter(user=user,deadline=datetime.date.today() + datetime.timedelta(days=1))
        tasks_the_day_after_tomorrow = Task.objects.filter(user=user,deadline=datetime.date.today() + datetime.timedelta(days=2))
        response = render_block_to_string("home.html", "tasks", {"today":tasks_today,
                                                                                                        "tomorrow":tasks_tomorrow,
                                                                                                        "the_day_after_tomorrow":tasks_the_day_after_tomorrow})
        return HttpResponse(response)


class EditTaskPage(TemplateView):
    template_name = "task.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Task.objects.filter(id=kwargs["pk"])
        context["old_text"] = task.text
        context["old_deadline"] = task.deadline
        context["old_priority"] = task.priority
        context["old_state"] = task.done
        return context

    def post(self,request,**kwargs):
        data = request.POST
        print(data)
        task = Task.objects.filter(id=kwargs["pk"])
        if data.get("new_task_text") is not None:
            task.update(text=data.get("new_task_text"))
        if data.get("new_task_deadline") is not None:
            task.update(deadline=data.get("new_task_deadline"))
        if data.get("new_task_priority") is not None:
            task.update(priority=data.get("new_task_priority"))
        if data.get("new_task_state") is not None:
            task.update(done=data.get("new_task_state"))
        response = render_block_to_string("task.html", "task", {"old_text": task.text,
                                                                 "old_deadline": task.deadline,
                                                                 "old_priority": task.priority,
                                                                 "old_state": task.done})
        return HttpResponse(response)


class ProfileEditPage(TemplateView):
    template_name = "profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(id=self.kwargs["pk"])
        context["username"] = user
        context["email"] = user.email
        return context

    def post(self,request,**kwargs):
        data = request.POST
        user = request.user
        new_username = data.get("new_username")
        new_email = data.get("new_email")
        user.update(username=new_username,email=new_email)
        response = render_block_to_string("profile.html", "user", {"username": user.username,
                                                                "email": user.email})
        return HttpResponse(response)

def Logout(request):
    logout(request)
    return redirect("/")




