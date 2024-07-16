from  django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views. RegistrationPage.as_view(), name = 'Registration'),
    path('login/', views.LoginPage.as_view(), name = 'Login'),
    path('home/', views.HomePage.as_view(), name = 'Home'),
    path('tasklist/', views.TaskListPage.as_view(), name = 'TaskList'),
    path('profile/', views.ProfileEditPage.as_view(), name = 'Profile'),
    path('createtask/', views.CreateTaskPage.as_view(), name = 'CreateTask'),
    path('edittask/<int:pk>', views.EditTaskPage.as_view(), name = 'EditTask'),
    path('logout/', views.Logout, name = 'Logout')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)