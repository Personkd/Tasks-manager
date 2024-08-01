from django import forms
from  django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Task
class User_class(UserCreationForm):
    class Meta:
        model = User
        fields= ["username","email","password1","password2"]

class Login_class(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class Create_task_class(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["text"].widget.attrs.update(size="80")
    class Meta:
        #priorities = [
       #     ("Low", "Low"),
        #    ("Medium", "Medium"),
        #    ("High", "High")
       # ]
        model = Task
        fields = ["text", "deadline", "priority"]
        #widgets = {
         #'text': forms.CharField
         #"deadline":forms.DateField(),
        #"priority":forms.ChoiceField(choices=priorities)
       #}