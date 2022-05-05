from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


app_name = 'account'

urlpatterns = [
    # path('login/', views.user_login, name="login"),
    # path('logout/', views.user_logout, name="logout"),
    path('login/', auth_views.LoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="registration/logged_out.html"), name='logout'),
    path('', views.user_dashboard, name="dashboard"),
    path('register/', views.user_register, name="register"),
]
