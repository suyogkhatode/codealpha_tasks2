from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("profile/", views.profile, name="profile"),
    path("user/<str:username>/", views.user_profile, name="user_profile"),
    path("follow/<str:username>/", views.follow_user, name="follow_user"),
]