from  django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views. RegistrationPage.as_view(), name = 'Registration'),
    path('login/', views.LoginPage.as_view(), name = 'Login'),
    path('home/', views.HomePage.as_view(), name = 'Home'),
    #path('tasklist/', views.TaskListPage, name = 'TaskList'),
    #path('profileedit/', views.ProfileEditPage, name = 'ProfileEdit'),
    #path('createtask/', views.CreateTaskPage, name = 'CreateTask'),
    #path('edittask/', views.EditTaskPage, name = 'EditTask'),
    path('logout/', views.Logout, name = 'Logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)