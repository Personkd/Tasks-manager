from django import forms
from  django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
class User_class(UserCreationForm):
    class Meta:
        model = User
        fields= ["username","email","password1","password2"]

class Login_class(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]